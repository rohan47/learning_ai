"""Main FastAPI application for ADHD Focus Hub."""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import asyncio
import logging
import sys
import os
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to the path to resolve imports
sys.path.append(str(Path(__file__).parent.parent))

from crew.crew import ADHDFocusHubCrew
from api.models import *

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global crew instance
crew_instance = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    global crew_instance
    try:
        logger.info("Initializing ADHD Focus Hub CrewAI system...")
        crew_instance = ADHDFocusHubCrew()
        logger.info("CrewAI system initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize CrewAI system: {e}")
        crew_instance = None
    
    yield
    
    # Shutdown
    logger.info("Shutting down ADHD Focus Hub API")
    crew_instance = None


# Create FastAPI app
app = FastAPI(
    title="ADHD Focus Hub API",
    description="AI-powered ADHD management system with CrewAI multi-agent support",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "https://your-frontend-domain.com"  # Production domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer(auto_error=False)


# Dependency to get crew instance
def get_crew() -> ADHDFocusHubCrew:
    """Get the crew instance."""
    if crew_instance is None:
        raise HTTPException(
            status_code=503, 
            detail="CrewAI system not initialized. Please try again later."
        )
    return crew_instance


# Basic endpoints
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "message": "ADHD Focus Hub API - CrewAI Powered",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy" if crew_instance is not None else "degraded",
        crew_initialized=crew_instance is not None,
        version="1.0.0"
    )


# Main chat endpoint - routes to appropriate agents
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_with_agents(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    crew: ADHDFocusHubCrew = Depends(get_crew)
):
    """Main chat endpoint that routes requests to appropriate AI agents."""
    try:
        # Route request through CrewAI
        result = await crew.async_route_request(
            request.message,
            request.context
        )
        
        # Log interaction for learning (background task)
        background_tasks.add_task(
            log_interaction,
            input_message=request.message,
            output=result,
            context=request.context
        )
        
        return ChatResponse(
            response=result["response"],
            agent_used=result["primary_agent"],
            confidence=result.get("confidence", 0.9),
            suggestions=result.get("suggestions", []),
            metadata=result.get("metadata", {})
        )
        
    except Exception as e:
        logger.error(f"Agent processing error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Agent processing error: {str(e)}"
        )


# Comprehensive consultation endpoint
@app.post("/api/v1/chat/comprehensive", response_model=ChatResponse)
async def comprehensive_chat_consultation(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    crew: ADHDFocusHubCrew = Depends(get_crew)
):
    """Comprehensive consultation endpoint that uses orchestrator with multiple agents."""
    try:
        # Use comprehensive consultation with orchestrator
        result = await asyncio.get_event_loop().run_in_executor(
            None, crew.comprehensive_consultation, request.message, request.context
        )
        
        # Log interaction for learning (background task)
        background_tasks.add_task(
            log_interaction,
            input_message=request.message,
            output=result,
            context=request.context
        )
        
        return ChatResponse(
            response=result["response"],
            agent_used=result.get("metadata", {}).get("consultation_type", "orchestrator"),
            confidence=result.get("confidence", 0.95),
            suggestions=result.get("suggestions", []),
            metadata=result.get("metadata", {})
        )
        
    except Exception as e:
        logger.error(f"Comprehensive consultation error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Comprehensive consultation error: {str(e)}"
        )


# Task breakdown endpoint
@app.post("/api/v1/tasks/breakdown", response_model=TaskBreakdownResponse)
async def breakdown_task(
    request: TaskBreakdownRequest,
    crew: ADHDFocusHubCrew = Depends(get_crew)
):
    """Break down a complex task into ADHD-friendly steps."""
    try:
        planning_agent = crew.agents["planning"]
        
        result = planning_agent.process_task_breakdown(
            user_input=f"{request.title}: {request.description or ''}",
            context={
                "priority": request.priority,
                "estimated_duration": request.estimated_duration
            }
        )
        
        # Convert to response format
        return TaskBreakdownResponse(
            subtasks=[],  # Would be populated from result
            total_estimated_minutes=result.get("estimated_minutes", 60),
            difficulty_assessment=result.get("difficulty_level", "moderate"),
            adhd_tips=result.get("adhd_tips", []),
            recommended_focus_sessions=result.get("estimated_sessions", 2)
        )
        
    except Exception as e:
        logger.error(f"Task breakdown error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Task breakdown error: {str(e)}"
        )


# Focus session endpoint
@app.post("/api/v1/focus/start", response_model=FocusSessionResponse)
async def start_focus_session(
    request: FocusSessionRequest,
    crew: ADHDFocusHubCrew = Depends(get_crew)
):
    """Start an adaptive focus session."""
    try:
        focus_agent = crew.agents["focus"]
        
        result = focus_agent.start_focus_session(
            task=request.task_description,
            duration=request.requested_duration,
            context={
                "distraction_level": request.distraction_level,
                "task_id": request.task_id
            }
        )
        
        # Generate unique session ID
        import uuid
        session_id = str(uuid.uuid4())
        
        return FocusSessionResponse(
            session_id=session_id,
            adapted_duration=result.get("recommended_duration", request.requested_duration),
            break_schedule=[],  # Would be populated from result
            focus_techniques=result.get("focus_techniques", []),
            environment_suggestions=result.get("environment_tips", [])
        )
        
    except Exception as e:
        logger.error(f"Focus session error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Focus session error: {str(e)}"
        )


# Mood tracking endpoint
@app.post("/api/v1/mood/log", response_model=MoodCheckResponse)
async def log_mood(
    request: MoodCheckRequest,
    crew: ADHDFocusHubCrew = Depends(get_crew)
):
    """Log mood and get emotional support."""
    try:
        emotion_agent = crew.agents["emotion"]
        
        mood_data = {
            "mood_score": request.mood_score,
            "energy_level": request.energy_level,
            "stress_level": request.stress_level,
            "notes": request.notes,
            "triggers": request.triggers
        }
        
        result = emotion_agent.process_mood_check(mood_data)
        
        return MoodCheckResponse(
            analysis=result.get("response", "Mood logged successfully"),
            coping_strategies=[],  # Would be populated from result
            recommended_activities=result.get("suggestions", []),
            escalation_needed=result.get("follow_up_recommended", False)
        )
        
    except Exception as e:
        logger.error(f"Mood logging error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Mood logging error: {str(e)}"
        )


# Agent status endpoint
@app.get("/api/v1/agents/status", response_model=SystemStatus)
async def get_agent_status(crew: ADHDFocusHubCrew = Depends(get_crew)):
    """Get status of all AI agents."""
    try:
        status = crew.get_agent_status()
        
        # Convert to response format
        agents_status = {}
        for agent_name, agent_info in status["agents"].items():
            agents_status[agent_name] = AgentStatus(
                role=agent_info["role"],
                total_interactions=agent_info["total_interactions"],
                available=agent_info["available"]
            )
        
        return SystemStatus(
            total_agents=status["total_agents"],
            agents=agents_status,
            total_conversations=status["total_conversations"],
            system_uptime=status["system_uptime"]
        )
        
    except Exception as e:
        logger.error(f"Agent status error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Agent status error: {str(e)}"
        )


# Cache management endpoints
@app.post("/api/v1/system/clear-cache")
async def clear_cache(crew: ADHDFocusHubCrew = Depends(get_crew)):
    """Clear conversation history and agent cache to resolve routing conflicts."""
    try:
        crew.clear_conversation_history()
        return {"message": "Cache cleared successfully", "timestamp": datetime.utcnow().isoformat()}
        
    except Exception as e:
        logger.error(f"Cache clear error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Cache clear error: {str(e)}"
        )


@app.post("/api/v1/system/refresh-agents")
async def refresh_agents(crew: ADHDFocusHubCrew = Depends(get_crew)):
    """Force refresh all agents to clear cached state."""
    try:
        crew.force_agent_refresh()
        return {"message": "All agents refreshed successfully", "timestamp": datetime.utcnow().isoformat()}
        
    except Exception as e:
        logger.error(f"Agent refresh error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Agent refresh error: {str(e)}"
        )


# Enhanced chat endpoint with cache busting
@app.post("/api/v1/chat/fresh")
async def chat_fresh(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    crew: ADHDFocusHubCrew = Depends(get_crew)
):
    """Chat endpoint that forces fresh responses by clearing relevant cache."""
    try:
        # Clear recent conversation history to prevent routing conflicts
        if len(crew.conversation_history) > 5:
            crew.conversation_history = crew.conversation_history[-2:]  # Keep only last 2
        
        # Route request through CrewAI
        result = await crew.async_route_request(
            request.message,
            request.context
        )
        
        # Log interaction for learning (background task)
        background_tasks.add_task(
            log_interaction,
            input_message=request.message,
            output=result,
            context=request.context
        )
        
        return ChatResponse(
            response=result["response"],
            agent_used=result["primary_agent"],
            confidence=result.get("confidence", 0.9),
            suggestions=result.get("suggestions", []),
            metadata=result.get("metadata", {})
        )
        
    except Exception as e:
        logger.error(f"Fresh chat processing error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Fresh chat processing error: {str(e)}"
        )
        
    except Exception as e:
        logger.error(f"Agent status error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Agent status error: {str(e)}"
        )


# Conversation history endpoint
@app.get("/api/v1/conversations/summary")
async def get_conversation_summary(
    limit: int = 10,
    crew: ADHDFocusHubCrew = Depends(get_crew)
):
    """Get recent conversation summary."""
    try:
        summary = crew.get_conversation_summary(limit)
        return summary
    except Exception as e:
        logger.error(f"Conversation summary error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Conversation summary error: {str(e)}"
        )


# Background task for logging interactions
async def log_interaction(
    input_message: str,
    output: Dict[str, Any],
    context: Dict[str, Any] = None
):
    """Log user interaction for analytics and learning."""
    try:
        # This would typically save to database
        logger.info(f"Interaction logged: {len(input_message)} chars input, "
                   f"agent: {output.get('primary_agent', 'unknown')}")
    except Exception as e:
        logger.error(f"Failed to log interaction: {e}")


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return ErrorResponse(
        detail=exc.detail,
        error_code=str(exc.status_code)
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return ErrorResponse(
        detail="An unexpected error occurred. Please try again later.",
        error_code="500"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
