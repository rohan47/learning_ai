import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import MoodCheckRequest, MoodCheckResponse, MoodLogOut
from ..main import get_db
from database.models import MoodLog, User
from crew.crew import ADHDFocusHubCrew
from ..routes.auth import get_current_user
from ..main import get_crew

logger = logging.getLogger(__name__)

router = APIRouter(tags=["mood"])


@router.post("/api/v1/mood/log", response_model=MoodCheckResponse)
async def log_mood(
    request: MoodCheckRequest,
    crew: ADHDFocusHubCrew = Depends(get_crew),
):
    """Log mood and get emotional support."""
    try:
        emotion_agent = crew.agents["emotion"]

        mood_data = {
            "mood_score": request.mood_score,
            "energy_level": request.energy_level,
            "stress_level": request.stress_level,
            "notes": request.notes,
            "triggers": request.triggers,
        }

        result = emotion_agent.process_mood_check(mood_data)

        return MoodCheckResponse(
            analysis=result.get("response", "Mood logged successfully"),
            coping_strategies=[],
            recommended_activities=result.get("suggestions", []),
            escalation_needed=result.get("follow_up_recommended", False),
        )

    except Exception as e:
        logger.error(f"Mood logging error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Mood logging error: {str(e)}")


@router.post("/api/v1/moods", response_model=MoodLogOut)
async def create_mood(
    log: MoodCheckRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    entry = MoodLog(owner_id=current_user.id, mood_score=log.mood_score, notes=log.notes)
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


@router.get("/api/v1/moods", response_model=list[MoodLogOut])
async def list_moods(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(MoodLog).where(MoodLog.owner_id == current_user.id))
    return result.scalars().all()
