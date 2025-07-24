import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import (
    TaskBreakdownRequest,
    TaskBreakdownResponse,
    FocusSessionRequest,
    FocusSessionResponse,
    TaskCreate,
    TaskOut,
)
from ..main import get_db
from backend.database.models import Task, User
from crew.crew import ADHDFocusHubCrew
from ..routes.auth import get_current_user
from ..main import get_crew

logger = logging.getLogger(__name__)

router = APIRouter(tags=["tasks"])


@router.post("/api/v1/tasks/breakdown", response_model=TaskBreakdownResponse)
async def breakdown_task(
    request: TaskBreakdownRequest,
    crew: ADHDFocusHubCrew = Depends(get_crew),
):
    """Break down a complex task into ADHD-friendly steps."""
    try:
        planning_agent = crew.agents["planning"]

        result = planning_agent.process_task_breakdown(
            user_input=f"{request.title}: {request.description or ''}",
            context={
                "priority": request.priority,
                "estimated_duration": request.estimated_duration,
            },
        )

        return TaskBreakdownResponse(
            subtasks=[],
            total_estimated_minutes=result.get("estimated_minutes", 60),
            difficulty_assessment=result.get("difficulty_level", "moderate"),
            adhd_tips=result.get("adhd_tips", []),
            recommended_focus_sessions=result.get("estimated_sessions", 2),
        )

    except Exception as e:
        logger.error(f"Task breakdown error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Task breakdown error: {str(e)}")


@router.post("/api/v1/focus/start", response_model=FocusSessionResponse)
async def start_focus_session(
    request: FocusSessionRequest,
    crew: ADHDFocusHubCrew = Depends(get_crew),
):
    """Start an adaptive focus session."""
    try:
        focus_agent = crew.agents["focus"]

        result = focus_agent.start_focus_session(
            task=request.task_description,
            duration=request.requested_duration,
            context={
                "distraction_level": request.distraction_level,
                "task_id": request.task_id,
            },
        )

        session_id = str(uuid.uuid4())

        return FocusSessionResponse(
            session_id=session_id,
            adapted_duration=result.get("recommended_duration", request.requested_duration),
            break_schedule=[],
            focus_techniques=result.get("focus_techniques", []),
            environment_suggestions=result.get("environment_tips", []),
        )

    except Exception as e:
        logger.error(f"Focus session error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Focus session error: {str(e)}")


@router.post("/api/v1/tasks", response_model=TaskOut)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    new_task = Task(owner_id=current_user.id, title=task.title, description=task.description)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.get("/api/v1/tasks", response_model=list[TaskOut])
async def list_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Task).where(Task.owner_id == current_user.id))
    return result.scalars().all()


@router.delete("/api/v1/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.owner_id == current_user.id))
    task_obj = result.scalar_one_or_none()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task_obj)
    await db.commit()
    return {"status": "deleted"}
