"""Focus and attention management tools for ADHD support."""

from typing import Dict, Any, List, Type
import json
from datetime import datetime, timedelta

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class FocusSessionInput(BaseModel):
    task_name: str = Field(description="Name of the task to focus on")
    target_duration: int = Field(description="Target duration in minutes", default=25)
    difficulty_level: str = Field(description="Task difficulty level", default="medium")
    distractions: List[str] = Field(description="Known distractions", default=[])


class DistractionManagementInput(BaseModel):
    current_distractions: List[str] = Field(description="Current distractions")
    environment: str = Field(description="Current environment", default="home")
    urgency_level: int = Field(description="Task urgency 1-10", default=5)


class BreakOptimizationInput(BaseModel):
    work_duration: int = Field(description="Minutes worked", default=25)
    energy_level: int = Field(description="Energy level 1-10", default=5)
    next_task_type: str = Field(description="Type of next task", default="cognitive")


class FocusSessionTool(BaseTool):
    """Tool for creating ADHD-friendly focus sessions."""
    
    name: str = "focus_session"
    description: str = "Create personalized focus sessions with ADHD accommodations"
    args_schema: Type[BaseModel] = FocusSessionInput
    
    def _run(self, task_name: str, target_duration: int = 25, difficulty_level: str = "medium", distractions: List[str] = []) -> str:
        """Create a focus session plan."""
        
        # Adjust duration based on ADHD considerations
        if difficulty_level == "high":
            adjusted_duration = min(target_duration, 20)  # Cap at 20 min for high difficulty
        elif difficulty_level == "low":
            adjusted_duration = min(target_duration, 45)  # Can go longer for easy tasks
        else:
            adjusted_duration = min(target_duration, 25)  # Standard Pomodoro
        
        # Create focus session structure
        session = {
            "task": task_name,
            "duration": adjusted_duration,
            "structure": {
                "warm_up": "2 minutes - Clear workspace and set intention",
                "main_work": f"{adjusted_duration - 2} minutes - Deep work on {task_name}",
                "wrap_up": "Last minute - Note progress and next steps"
            },
            "adhd_strategies": [
                "🎯 Single-task focus only",
                "📱 Phone in another room or drawer",
                "⏰ Visible timer with gentle alert",
                "🎵 Background noise or focus music if helpful",
                "✅ Have a 'done' list ready for sense of accomplishment"
            ],
            "distraction_plan": self._create_distraction_plan(distractions),
            "success_metrics": [
                "Stayed on task for at least 80% of session",
                "Made measurable progress",
                "Maintained awareness of focus state"
            ]
        }
        
        return json.dumps(session, indent=2)
    
    def _create_distraction_plan(self, distractions: List[str]) -> Dict[str, str]:
        """Create strategies for managing specific distractions."""
        plans = {}
        
        for distraction in distractions:
            if "social media" in distraction.lower() or "phone" in distraction.lower():
                plans[distraction] = "Use app blockers or place device in another room"
            elif "noise" in distraction.lower() or "sound" in distraction.lower():
                plans[distraction] = "Use noise-canceling headphones or white noise"
            elif "email" in distraction.lower():
                plans[distraction] = "Close email client and set specific check times"
            elif "people" in distraction.lower() or "family" in distraction.lower():
                plans[distraction] = "Use 'Do Not Disturb' signals and communicate focus time"
            else:
                plans[distraction] = "Acknowledge the thought and gently redirect to task"
        
        return plans


class DistractionManagementTool(BaseTool):
    """Tool for managing ADHD-related distractions."""
    
    name: str = "distraction_management"
    description: str = "Provide strategies for managing distractions during focus time"
    args_schema: Type[BaseModel] = DistractionManagementInput
    
    def _run(self, current_distractions: List[str], environment: str = "home", urgency_level: int = 5) -> str:
        """Provide distraction management strategies."""
        
        strategies = {
            "immediate_actions": [],
            "environment_setup": [],
            "mindset_shifts": [],
            "emergency_refocus": []
        }
        
        # Immediate actions based on distractions
        for distraction in current_distractions:
            if any(word in distraction.lower() for word in ["phone", "social", "text"]):
                strategies["immediate_actions"].append("📱 Put phone in airplane mode or another room")
            elif "noise" in distraction.lower():
                strategies["immediate_actions"].append("🎧 Use noise-canceling headphones or earplugs")
            elif "clutter" in distraction.lower():
                strategies["immediate_actions"].append("🧹 Spend 2 minutes clearing immediate workspace")
            elif "hunger" in distraction.lower() or "thirst" in distraction.lower():
                strategies["immediate_actions"].append("🥤 Take care of basic needs first")
        
        # Environment-specific strategies
        if environment == "home":
            strategies["environment_setup"] = [
                "🚪 Close door if possible",
                "🪑 Designate a specific work chair/area",
                "📺 Turn off TV and other entertainment devices",
                "🧘 Create a 'focus ritual' to signal work time"
            ]
        elif environment == "office":
            strategies["environment_setup"] = [
                "🎧 Use headphones as a 'do not disturb' signal",
                "📧 Set email to offline mode",
                "🖥️ Close unnecessary browser tabs and applications",
                "☕ Have water and snacks nearby"
            ]
        
        # Urgency-based strategies
        if urgency_level >= 8:
            strategies["emergency_refocus"] = [
                "⏰ Use 10-minute micro-sessions",
                "🎯 Focus on ONE small action at a time",
                "📝 Write down distracting thoughts to address later",
                "🏃 Take 30 seconds to do jumping jacks if restless"
            ]
        else:
            strategies["emergency_refocus"] = [
                "🧘 Take 3 deep breaths",
                "🎯 Remind yourself of the 'why' behind the task",
                "✅ Celebrate small wins to build momentum",
                "🔄 Use body doubling (work alongside others virtually)"
            ]
        
        # Universal mindset shifts
        strategies["mindset_shifts"] = [
            "🌊 Distractions are normal with ADHD - be kind to yourself",
            "🎪 Treat focus like a muscle that gets stronger with practice",
            "🔄 Progress over perfection - any forward movement counts",
            "🎁 Each successful focus period is a gift to your future self"
        ]
        
        result = {
            "distraction_assessment": {
                "identified_distractions": current_distractions,
                "environment": environment,
                "urgency_level": urgency_level,
                "complexity_score": len(current_distractions) * (urgency_level / 10)
            },
            "management_strategies": strategies,
            "quick_wins": [
                "Start with just 5 minutes of focused work",
                "Use the '2-minute rule' for immediate distractions",
                "Celebrate awareness - noticing distractions IS progress"
            ]
        }
        
        return json.dumps(result, indent=2)


class BreakOptimizationTool(BaseTool):
    """Tool for optimizing break time for ADHD brains."""
    
    name: str = "break_optimization"
    description: str = "Suggest optimal break activities based on energy and next task type"
    args_schema: Type[BaseModel] = BreakOptimizationInput
    
    def _run(self, work_duration: int = 25, energy_level: int = 5, next_task_type: str = "cognitive") -> str:
        """Suggest optimal break activities."""
        
        # Calculate break duration
        if work_duration <= 25:
            break_duration = 5
        elif work_duration <= 45:
            break_duration = 10
        else:
            break_duration = 15
        
        # Adjust for energy level
        if energy_level <= 3:
            break_type = "restorative"
        elif energy_level >= 8:
            break_type = "calming"
        else:
            break_type = "balanced"
        
        activities = {
            "restorative": [
                "🧘 2-minute breathing exercise",
                "🚶 Light walk around the room or outside",
                "🥤 Hydrate and have a healthy snack",
                "🌅 Look out a window or step outside briefly",
                "🎵 Listen to one energizing song"
            ],
            "calming": [
                "🧘 Progressive muscle relaxation",
                "📖 Read a few pages of fiction",
                "🎨 Doodle or do a quick creative activity",
                "🌿 Tend to plants or organize a small space",
                "☕ Make tea mindfully"
            ],
            "balanced": [
                "🤸 Light stretching or yoga poses",
                "📱 Quick chat with a friend or family member",
                "🧹 Tidy workspace for next session",
                "📝 Journal about progress or feelings",
                "🎮 Play a quick puzzle game"
            ]
        }
        
        # Avoid screens before cognitive tasks
        screen_warning = ""
        if next_task_type in ["cognitive", "creative", "analytical"]:
            screen_warning = "⚠️ Avoid screens during this break to maintain focus for your next cognitive task"
        
        # Special ADHD considerations
        adhd_tips = [
            "⏰ Set a timer for your break to avoid time blindness",
            "🚫 Avoid activities that might lead to hyperfocus",
            "🔄 Move your body - ADHD brains need movement",
            "💧 Stay hydrated - dehydration affects focus",
            "🎯 Keep breaks intentional, not reactive"
        ]
        
        result = {
            "break_plan": {
                "duration": f"{break_duration} minutes",
                "type": break_type,
                "recommended_activities": activities[break_type],
                "screen_guidance": screen_warning if screen_warning else "Screens OK in moderation",
                "transition_back": "Spend 30 seconds reviewing what you accomplished and setting intention for next session"
            },
            "adhd_considerations": adhd_tips,
            "energy_assessment": {
                "current_level": energy_level,
                "post_break_target": min(energy_level + 1, 10) if energy_level <= 5 else max(energy_level - 1, 6),
                "next_task_readiness": "optimal" if 4 <= energy_level <= 7 else "adjust_expectations"
            }
        }
        
        return json.dumps(result, indent=2)
