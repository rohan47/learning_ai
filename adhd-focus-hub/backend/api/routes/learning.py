import logging
from fastapi import APIRouter, Depends, HTTPException

from api.models import LearningRequest, LearningResponse
from crew.crew import ADHDFocusHubCrew
from ..main import get_crew

logger = logging.getLogger(__name__)

router = APIRouter(tags=["learning"])


@router.post("/api/v1/learn", response_model=LearningResponse)
async def learn(
    request: LearningRequest,
    crew: ADHDFocusHubCrew = Depends(get_crew),
):
    """Provide ADHD-optimized learning guidance."""
    try:
        learning_agent = crew.agents["learning"]
        result = learning_agent.create_learning_plan(
            request.subject,
            request.learning_goals,
            context={
                "current_level": request.current_level,
                "available_time": request.available_time,
            },
        )
        return LearningResponse(
            learning_plan=result.get("response", ""),
            study_sessions=result.get("optimal_study_sessions", {}),
            retention_methods=result.get("retention_strategies", []),
            motivation_hooks=result.get("motivation_hooks", []),
        )
    except Exception as e:
        logger.error(f"Learning error: {e}")
        raise HTTPException(status_code=500, detail=f"Learning error: {e}")
