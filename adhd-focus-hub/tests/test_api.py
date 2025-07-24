import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:////tmp/test.db"

from backend.api.main import app, get_db
from backend.database import Base, engine, SessionLocal


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
            json={"mood_score": 5, "energy_level": 5, "stress_level": 5, "notes": "ok", "triggers": []},
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

