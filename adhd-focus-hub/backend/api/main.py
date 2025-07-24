"""Main FastAPI application for ADHD Focus Hub."""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import asyncio
import logging
import sys
import os
from pathlib import Path
from typing import Dict, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from database.models import User, Task, MoodLog

# Load environment variables from backend/.env if present
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# Add the parent directory to the path to resolve imports
sys.path.append(str(Path(__file__).parent.parent))

from crew.crew import ADHDFocusHubCrew
from api.models import *

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global crew instance
crew_instance = None

# Auth settings
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def authenticate_user(db: AsyncSession, username: str, password: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


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


@app.post("/api/v1/auth/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.username == user.username))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(username=user.username, hashed_password=get_password_hash(user.password))
    db.add(new_user)
    await db.commit()
    access_token = create_access_token({"sub": new_user.username})
    return Token(access_token=access_token)


@app.post("/api/v1/auth/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.username})
    return Token(access_token=token)


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


# CRUD endpoints for tasks
@app.post("/api/v1/tasks", response_model=TaskOut)
async def create_task(task: TaskCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    new_task = Task(owner_id=current_user.id, title=task.title, description=task.description)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@app.get("/api/v1/tasks", response_model=list[TaskOut])
async def list_tasks(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.owner_id == current_user.id))
    return result.scalars().all()


@app.delete("/api/v1/tasks/{task_id}")
async def delete_task(task_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.owner_id == current_user.id))
    task_obj = result.scalar_one_or_none()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task_obj)
    await db.commit()
    return {"status": "deleted"}


# CRUD endpoints for mood logs
@app.post("/api/v1/moods", response_model=MoodLogOut)
async def create_mood(log: MoodCheckRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    entry = MoodLog(owner_id=current_user.id, mood_score=log.mood_score, notes=log.notes)
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


@app.get("/api/v1/moods", response_model=list[MoodLogOut])
async def list_moods(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MoodLog).where(MoodLog.owner_id == current_user.id))
    return result.scalars().all()


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
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            ErrorResponse(
                detail=exc.detail,
                error_code=str(exc.status_code),
            )
        ),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            ErrorResponse(
                detail="An unexpected error occurred. Please try again later.",
                error_code="500",
            )
        ),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
