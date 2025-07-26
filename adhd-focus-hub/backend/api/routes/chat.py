import asyncio
import logging
from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from api.models import (
    ChatRequest,
    ChatResponse,
    AgentStatus,
    SystemStatus,
    ConversationRecord,
)
from crew.crew import ADHDFocusHubCrew
from database import SessionLocal
from database.models import ConversationHistory
from services.cache import push_history, get_history
from ..main import get_crew

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"])


async def log_interaction(
    input_message: str,
    output: Dict[str, Any],
    context: Dict[str, Any] | None = None,
) -> None:
    """Persist interaction in the database and cache."""
    try:
        user_id = context.get("user_id") if context else None
        record_data = {
            "message": input_message,
            "response": output.get("response", ""),
            "metadata": output.get("metadata", {}),
        }

        async with SessionLocal() as session:
            obj = ConversationHistory(
                user_id=user_id,
                message=record_data["message"],
                response=record_data["response"],
                metadata_json=record_data["metadata"],
            )
            session.add(obj)
            await session.commit()
            await session.refresh(obj)

            record_data.update(
                {
                    "id": obj.id,
                    "user_id": obj.user_id,
                    "created_at": obj.created_at.isoformat(),
                }
            )

        await push_history(user_id, record_data)

        logger.info(
            "Interaction logged: %s chars input, agent: %s",
            len(input_message),
            output.get("primary_agent", "unknown"),
        )
    except Exception as e:
        logger.error(f"Failed to log interaction: {e}")


@router.post("/api/v1/chat", response_model=ChatResponse)
async def chat_with_agents(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    crew: ADHDFocusHubCrew = Depends(get_crew),
):
    """Main chat endpoint that routes requests to appropriate AI agents."""
    try:
        result = await crew.async_route_request(request.message, request.context)
        background_tasks.add_task(
            log_interaction, request.message, result, request.context
        )
        return ChatResponse(
            response=result["response"],
            agent_used=result["primary_agent"],
            confidence=result.get("confidence", 0.9),
            suggestions=result.get("suggestions", []),
            metadata=result.get("metadata", {}),
        )
    except Exception as e:
        logger.error(f"Agent processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Agent processing error: {str(e)}")


@router.post("/api/v1/chat/comprehensive", response_model=ChatResponse)
async def comprehensive_chat_consultation(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    crew: ADHDFocusHubCrew = Depends(get_crew),
):
    """Comprehensive consultation endpoint that uses orchestrator."""
    try:
        result = await asyncio.get_event_loop().run_in_executor(
            None, crew.comprehensive_consultation, request.message, request.context
        )
        background_tasks.add_task(
            log_interaction, request.message, result, request.context
        )
        return ChatResponse(
            response=result["response"],
            agent_used=result.get("metadata", {}).get(
                "consultation_type", "orchestrator"
            ),
            confidence=result.get("confidence", 0.95),
            suggestions=result.get("suggestions", []),
            metadata=result.get("metadata", {}),
        )
    except Exception as e:
        logger.error(f"Comprehensive consultation error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Comprehensive consultation error: {str(e)}"
        )


@router.post("/api/v1/chat/fresh", response_model=ChatResponse)
async def chat_fresh(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    crew: ADHDFocusHubCrew = Depends(get_crew),
):
    """Chat endpoint that forces fresh responses by clearing relevant cache."""
    try:
        if len(crew.conversation_history) > 5:
            crew.conversation_history = crew.conversation_history[-2:]
        result = await crew.async_route_request(request.message, request.context)
        background_tasks.add_task(
            log_interaction, request.message, result, request.context
        )
        return ChatResponse(
            response=result["response"],
            agent_used=result["primary_agent"],
            confidence=result.get("confidence", 0.9),
            suggestions=result.get("suggestions", []),
            metadata=result.get("metadata", {}),
        )
    except Exception as e:
        logger.error(f"Fresh chat processing error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Fresh chat processing error: {str(e)}"
        )


@router.get("/api/v1/agents/status", response_model=SystemStatus)
async def get_agent_status(crew: ADHDFocusHubCrew = Depends(get_crew)):
    """Get status of all AI agents."""
    try:
        status = crew.get_agent_status()
        agents_status = {
            name: AgentStatus(
                role=info["role"],
                total_interactions=info["total_interactions"],
                available=info["available"],
            )
            for name, info in status["agents"].items()
        }
        return SystemStatus(
            total_agents=status["total_agents"],
            agents=agents_status,
            total_conversations=status["total_conversations"],
            system_uptime=status["system_uptime"],
        )
    except Exception as e:
        logger.error(f"Agent status error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Agent status error: {str(e)}")


@router.post("/api/v1/system/clear-cache")
async def clear_cache(crew: ADHDFocusHubCrew = Depends(get_crew)):
    """Clear conversation history and agent cache."""
    try:
        crew.clear_conversation_history()
        return {
            "message": "Cache cleared successfully",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Cache clear error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Cache clear error: {str(e)}")


@router.post("/api/v1/system/refresh-agents")
async def refresh_agents(crew: ADHDFocusHubCrew = Depends(get_crew)):
    """Force refresh all agents to clear cached state."""
    try:
        crew.force_agent_refresh()
        return {
            "message": "All agents refreshed successfully",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Agent refresh error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Agent refresh error: {str(e)}")


@router.get("/api/v1/conversations/summary")
async def get_conversation_summary(
    limit: int = 10, crew: ADHDFocusHubCrew = Depends(get_crew)
):
    """Get recent conversation summary."""
    try:
        return crew.get_conversation_summary(limit)
    except Exception as e:
        logger.error(f"Conversation summary error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Conversation summary error: {str(e)}"
        )


@router.get("/api/v1/conversations/history", response_model=list[ConversationRecord])
async def get_conversation_history(limit: int = 20):
    """Retrieve recent conversation history from Redis."""
    try:
        return await get_history(None, limit)
    except Exception as e:
        logger.error(f"Conversation history error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Conversation history error: {str(e)}"
        )
