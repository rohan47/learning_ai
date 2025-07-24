"""API models for ADHD Focus Hub."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class TaskPriority(str, Enum):
    """Task priority levels."""
    low = "low"
    medium = "medium" 
    high = "high"
    urgent = "urgent"


class TaskStatus(str, Enum):
    """Task completion status."""
    todo = "todo"
    in_progress = "in_progress"
    completed = "completed"
    blocked = "blocked"


class AgentType(str, Enum):
    """Available agent types."""
    planning = "planning"
    focus = "focus"
    emotion = "emotion"
    organize = "organize"
    learning = "learning"


# Chat Models
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    agent_preference: Optional[AgentType] = Field(default=None, description="Preferred agent")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Agent response")
    agent_used: str = Field(..., description="Primary agent that handled the request")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Response confidence score")
    suggestions: List[str] = Field(default=[], description="Follow-up suggestions")
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Task Management Models
class TaskBreakdownRequest(BaseModel):
    """Request for task breakdown."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(default=None, max_length=1000, description="Task description")
    priority: TaskPriority = Field(default=TaskPriority.medium, description="Task priority")
    estimated_duration: Optional[int] = Field(default=None, ge=5, le=480, description="Estimated duration in minutes")


class SubTask(BaseModel):
    """Sub-task model."""
    step: int = Field(..., ge=1, description="Step number")
    title: str = Field(..., description="Sub-task title")
    description: str = Field(..., description="Sub-task description")
    estimated_minutes: int = Field(..., ge=1, description="Estimated time in minutes")
    adhd_tips: List[str] = Field(default=[], description="ADHD-specific tips")


class TaskBreakdownResponse(BaseModel):
    """Response for task breakdown."""
    subtasks: List[SubTask] = Field(..., description="List of sub-tasks")
    total_estimated_minutes: int = Field(..., description="Total estimated time")
    difficulty_assessment: str = Field(..., description="Overall difficulty level")
    adhd_tips: List[str] = Field(default=[], description="General ADHD tips")
    recommended_focus_sessions: int = Field(..., description="Recommended number of focus sessions")


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Focus Session Models
class FocusSessionRequest(BaseModel):
    """Request for focus session."""
    task_id: Optional[str] = Field(default=None, description="Associated task ID")
    task_description: str = Field(..., min_length=1, max_length=500, description="Task to focus on")
    requested_duration: Optional[int] = Field(default=25, ge=15, le=90, description="Requested duration in minutes")
    distraction_level: Optional[int] = Field(default=None, ge=1, le=10, description="Current distraction level")


class BreakSchedule(BaseModel):
    """Break schedule item."""
    after_minutes: int = Field(..., description="When to take the break")
    type: str = Field(..., description="Type of break")
    duration: int = Field(..., description="Break duration in minutes")
    activities: List[str] = Field(default=[], description="Suggested break activities")


class FocusSessionResponse(BaseModel):
    """Response for focus session."""
    session_id: str = Field(..., description="Unique session identifier")
    adapted_duration: int = Field(..., description="AI-adapted duration")
    break_schedule: List[BreakSchedule] = Field(default=[], description="Recommended break schedule")
    focus_techniques: List[str] = Field(default=[], description="Suggested focus techniques")
    environment_suggestions: List[str] = Field(default=[], description="Environment optimization tips")


# Mood Tracking Models
class MoodCheckRequest(BaseModel):
    """Request for mood check-in."""
    mood_score: int = Field(..., ge=1, le=10, description="Mood rating 1-10")
    energy_level: int = Field(..., ge=1, le=10, description="Energy level 1-10")
    stress_level: int = Field(..., ge=1, le=10, description="Stress level 1-10")
    notes: Optional[str] = Field(default=None, max_length=1000, description="Additional notes")
    triggers: List[str] = Field(default=[], description="Identified triggers")


class CopingStrategy(BaseModel):
    """Coping strategy model."""
    category: str = Field(..., description="Strategy category")
    strategy: str = Field(..., description="Strategy name")
    description: str = Field(..., description="Strategy description")
    time_needed: str = Field(..., description="Estimated time to implement")


class MoodCheckResponse(BaseModel):
    """Response for mood check-in."""
    analysis: str = Field(..., description="Mood analysis")
    coping_strategies: List[CopingStrategy] = Field(default=[], description="Recommended coping strategies")
    recommended_activities: List[str] = Field(default=[], description="Suggested activities")
    escalation_needed: bool = Field(default=False, description="Whether professional help is recommended")
    follow_up_time: Optional[datetime] = Field(default=None, description="Recommended follow-up time")


class MoodLogOut(BaseModel):
    id: int
    mood_score: int
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Organization Models
class OrganizationRequest(BaseModel):
    """Request for organization help."""
    area: str = Field(..., min_length=1, max_length=200, description="Area to organize")
    challenges: List[str] = Field(..., description="Current organization challenges")
    available_time: Optional[int] = Field(default=None, ge=5, le=240, description="Available time in minutes")


class OrganizationStep(BaseModel):
    """Organization step model."""
    step: int = Field(..., description="Step number")
    title: str = Field(..., description="Step title")
    description: str = Field(..., description="Step description")
    estimated_minutes: int = Field(..., description="Estimated time")
    tools_needed: List[str] = Field(default=[], description="Required tools/materials")


class OrganizationResponse(BaseModel):
    """Response for organization request."""
    system_overview: str = Field(..., description="Overview of the organization system")
    steps: List[OrganizationStep] = Field(..., description="Step-by-step instructions")
    maintenance_schedule: Dict[str, str] = Field(default={}, description="Maintenance recommendations")
    visual_aids: List[str] = Field(default=[], description="Suggested visual organization aids")


# Learning Models
class LearningRequest(BaseModel):
    """Request for learning assistance."""
    subject: str = Field(..., min_length=1, max_length=200, description="Subject to learn")
    learning_goals: List[str] = Field(..., description="Specific learning goals")
    current_level: Optional[str] = Field(default="beginner", description="Current knowledge level")
    available_time: Optional[int] = Field(default=None, ge=15, le=480, description="Available study time per session")


class LearningMethod(BaseModel):
    """Learning method model."""
    method: str = Field(..., description="Learning method name")
    description: str = Field(..., description="Method description")
    adhd_twist: str = Field(..., description="ADHD-specific adaptation")


class LearningResponse(BaseModel):
    """Response for learning request."""
    learning_plan: str = Field(..., description="Personalized learning plan")
    study_sessions: Dict[str, Any] = Field(default={}, description="Recommended study session structure")
    retention_methods: List[LearningMethod] = Field(default=[], description="Memory retention strategies")
    motivation_hooks: List[str] = Field(default=[], description="Interest and motivation hooks")


# Agent Status Models
class AgentStatus(BaseModel):
    """Individual agent status."""
    role: str = Field(..., description="Agent role")
    total_interactions: int = Field(..., description="Total interactions")
    available: bool = Field(..., description="Agent availability")


class SystemStatus(BaseModel):
    """Overall system status."""
    total_agents: int = Field(..., description="Total number of agents")
    agents: Dict[str, AgentStatus] = Field(..., description="Individual agent statuses")
    total_conversations: int = Field(..., description="Total system conversations")
    system_uptime: str = Field(..., description="System uptime timestamp")


# Error Models
class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(..., description="Error description")
    error_code: Optional[str] = Field(default=None, description="Specific error code")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Health Check Model
class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="System health status")
    crew_initialized: bool = Field(..., description="Whether CrewAI is initialized")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
