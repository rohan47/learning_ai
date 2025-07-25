import logging
from fastapi import APIRouter, Depends, HTTPException

from api.models import OrganizationRequest, OrganizationResponse
from crew.crew import ADHDFocusHubCrew
from ..main import get_crew

logger = logging.getLogger(__name__)

router = APIRouter(tags=["organize"])


@router.post("/api/v1/organize", response_model=OrganizationResponse)
async def organize(
    request: OrganizationRequest,
    crew: ADHDFocusHubCrew = Depends(get_crew),
):
    """Provide ADHD-friendly organization plan."""
    try:
        organize_agent = crew.agents["organize"]
        result = organize_agent.create_organization_system(
            request.area,
            request.challenges,
            context={"available_time": request.available_time},
        )
        return OrganizationResponse(
            system_overview=result.get("response", ""),
            steps=[],
            maintenance_schedule=result.get("maintenance_frequency", {}),
            visual_aids=result.get("visual_elements", []),
        )
    except Exception as e:
        logger.error(f"Organization error: {e}")
        raise HTTPException(status_code=500, detail=f"Organization error: {e}")
