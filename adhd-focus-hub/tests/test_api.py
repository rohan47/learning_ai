import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:////tmp/test.db"

from backend.api.main import app, get_db, get_crew

# Import database objects using the same module path as the application.
# The app imports `database.models`, so we need to use the same package to
# ensure the SQLAlchemy Base instance is shared during testing.
from database import Base, engine, SessionLocal


@pytest.fixture(autouse=True, scope="module")
def setup_db():
    """Create and tear down database tables for tests."""
    import asyncio

    if os.path.exists("/tmp/test.db"):
        os.remove("/tmp/test.db")

    async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def teardown():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(init_db())
    yield
    asyncio.run(teardown())


async def get_test_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = get_test_db


def register_user(client, username="testuser", password="testpass"):
    resp = client.post(
        "/api/v1/auth/register",
        json={"username": username, "password": password},
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_registration_and_login():
    with TestClient(app) as client:
        token = register_user(client)
        resp = client.post(
            "/api/v1/auth/login",
            json={"username": "testuser", "password": "testpass"},
        )
        assert resp.status_code == 200
        assert "access_token" in resp.json()
        assert resp.json()["access_token"]


def test_task_crud_and_moods():
    with TestClient(app) as client:
        token = register_user(client, "taskuser", "taskpass")
        headers = {"Authorization": f"Bearer {token}"}

        resp = client.post(
            "/api/v1/tasks",
            json={"title": "Test Task", "description": "A task"},
            headers=headers,
        )
        assert resp.status_code == 200
        task = resp.json()

        resp = client.get("/api/v1/tasks", headers=headers)
        assert resp.status_code == 200
        assert len(resp.json()) == 1

        resp = client.post(
            "/api/v1/moods",
            json={
                "mood_score": 5,
                "energy_level": 5,
                "stress_level": 5,
                "notes": "ok",
                "triggers": [],
            },
            headers=headers,
        )
        assert resp.status_code == 200

        resp = client.get("/api/v1/moods", headers=headers)
        assert resp.status_code == 200
        assert len(resp.json()) == 1


def test_invalid_token():
    with TestClient(app) as client:
        resp = client.post(
            "/api/v1/tasks",
            json={"title": "Bad", "description": "Bad"},
            headers={"Authorization": "Bearer invalid"},
        )
        assert resp.status_code == 401


class DummyOrganizeAgent:
    def create_organization_system(self, area, challenges, context=None):
        return {
            "response": f"Organize {area}",
            "maintenance_frequency": {"daily": "5min tidy"},
            "visual_elements": ["labels"],
        }


class DummyLearningAgent:
    def create_learning_plan(self, subject, goals, context=None):
        return {
            "response": f"Learn {subject}",
            "optimal_study_sessions": {"recommended": "standard"},
            "retention_strategies": [],
            "motivation_hooks": ["hook"],
        }


class DummyCrew:
    def __init__(self):
        self.agents = {
            "organize": DummyOrganizeAgent(),
            "learning": DummyLearningAgent(),
        }


@pytest.fixture
def override_crew():
    crew = DummyCrew()
    app.dependency_overrides[get_crew] = lambda: crew
    yield
    app.dependency_overrides.pop(get_crew, None)


def test_organize_and_learn_endpoints(override_crew):
    with TestClient(app) as client:
        resp = client.post(
            "/api/v1/organize",
            json={"area": "desk", "challenges": ["clutter"], "available_time": 15},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "system_overview" in data
        assert "maintenance_schedule" in data
        assert "visual_aids" in data

        resp = client.post(
            "/api/v1/learn",
            json={"subject": "math", "learning_goals": ["algebra"]},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "learning_plan" in data
        assert "retention_methods" in data


class DummyChatCrew:
    async def async_route_request(self, message, context=None):
        return {"response": "ok", "primary_agent": "planning", "metadata": {}}


@pytest.fixture
def override_chat_crew():
    crew = DummyChatCrew()
    app.dependency_overrides[get_crew] = lambda: crew
    yield
    app.dependency_overrides.pop(get_crew, None)


def test_chat_history_persistence(monkeypatch, override_chat_crew):
    saved = {}

    async def fake_push(user_id, record):
        saved["record"] = record

    monkeypatch.setattr("backend.api.routes.chat.push_history", fake_push)

    with TestClient(app) as client:
        resp = client.post("/api/v1/chat", json={"message": "hello"})
        assert resp.status_code == 200

    import asyncio
    from sqlalchemy import select
    from database.models import ConversationHistory

    async def fetch():
        async with SessionLocal() as session:
            result = await session.execute(select(ConversationHistory))
            return result.scalars().all()

    records = asyncio.run(fetch())
    assert len(records) == 1
    assert records[0].message == "hello"
    assert saved["record"]["message"] == "hello"


def test_get_conversation_history(monkeypatch):
    async def fake_get_history(user_id, limit=20):
        return [
            {
                "id": 1,
                "user_id": None,
                "message": "hi",
                "response": "ok",
                "metadata": {},
                "created_at": "2024-01-01T00:00:00",
            }
        ]

    monkeypatch.setattr("backend.api.routes.chat.get_history", fake_get_history)

    with TestClient(app) as client:
        resp = client.get("/api/v1/conversations/history?limit=5")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert data[0]["message"] == "hi"
