"""Main FastAPI application for ADHD Focus Hub."""

import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import backend.database.models  # ensure models are registered
from api.models import ErrorResponse, HealthResponse
from backend.database import get_db
from config.settings import get_settings
from crew.crew import ADHDFocusHubCrew

# Load environment variables from backend/.env if present
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# Load application settings
settings = get_settings()

# Add the parent directory to the path to resolve imports
sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

crew_instance: ADHDFocusHubCrew | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global crew_instance
    try:
        logger.info("Initializing ADHD Focus Hub CrewAI system...")
        crew_instance = ADHDFocusHubCrew()
        logger.info("CrewAI system initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize CrewAI system: {e}")
        crew_instance = None
    yield
    logger.info("Shutting down ADHD Focus Hub API")
    crew_instance = None


app = FastAPI(
    title="ADHD Focus Hub API",
    description="AI-powered ADHD management system with CrewAI multi-agent support",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://your-frontend-domain.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_crew() -> ADHDFocusHubCrew:
    if crew_instance is None:
        raise HTTPException(
            status_code=503,
            detail="CrewAI system not initialized. Please try again later.",
        )
    return crew_instance


@app.get("/", response_model=Dict[str, str])
async def root():
    return {
        "message": "ADHD Focus Hub API - CrewAI Powered",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy" if crew_instance is not None else "degraded",
        crew_initialized=crew_instance is not None,
        version="1.0.0",
    )


from .routes.auth import router as auth_router
from .routes.chat import router as chat_router
from .routes.mood import router as mood_router
from .routes.tasks import router as tasks_router

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(tasks_router)
app.include_router(mood_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            ErrorResponse(detail=exc.detail, error_code=str(exc.status_code))
        ),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
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
