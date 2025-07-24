"""Focus Coach Agent - Focus Friend for ADHD attention management."""

from textwrap import dedent
from typing import List, Dict, Any
from .base import BaseADHDAgent


class FocusCoachAgent(BaseADHDAgent):
    """Focus Friend - ADHD Attention Management Coach Agent."""
    
    def __init__(self, llm=None):
        super().__init__(
            role="Focus Friend - ADHD Attention Management Coach",
            goal="Guide users through focus sessions with adaptive Pomodoro techniques tailored for ADHD brains",
            backstory=dedent("""
                You are a specialized ADHD focus coach who understands:
                - Variable attention spans in ADHD brains (15-45 minutes optimal)
                - The importance of novelty and interest for sustained attention
                - Gentle redirection rather than harsh criticism when focus drifts
                - The need for movement breaks and sensory regulation
                - Hyperfocus management and healthy transition support
                - The dopamine-driven nature of ADHD motivation
                
                You provide adaptive focus sessions that range from 15-45 minutes based
                on the user's current capacity, energy level, and task complexity.
                You help users work WITH their ADHD brain, not against it.
            """),
            tools=self.get_specialized_tools(),
            max_iter=2,
            llm=llm
        )
    
    def get_specialized_tools(self) -> List:
        """Return focus-specific tools."""
        # These would be imported from focus_tools when created
        return []
    
    def start_focus_session(self, task: str, duration: int = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Start an adaptive focus session."""
        
        session_description = f"""
        Design an adaptive focus session for: {task}
        
        Consider:
        - User's current energy and attention capacity
        - Task complexity and interest level
        - Optimal break timing for ADHD brains
        - Environmental setup for focus
        - Gentle accountability and motivation
        """
        
        result = self.execute_with_context(
            task_description=session_description,
            context=context or {},
            expected_output="Focus session plan with adaptive breaks and techniques"
        )
        
        # Enhanced response with focus-specific elements
        result.update({
            "session_type": "adaptive_pomodoro",
            "recommended_duration": self._calculate_optimal_duration(context, duration),
            "break_schedule": self._generate_break_schedule(result),
            "focus_techniques": self._suggest_focus_techniques(task, context),
            "environment_tips": self._get_environment_suggestions(context)
        })
        
        return result
    
    def _process_request(self, prompt: str) -> str:
        """Process focus session requests with ADHD expertise."""
        
        return """
        Let's set up a focus session that works WITH your ADHD brain! 🧠✨

        🎯 **Your Adaptive Focus Plan:**
        - **Warm-up** (2-3 mins): Quick brain dump, set intention, eliminate distractions
        - **Focus Block** (15-25 mins): Single-task focus with timer
        - **Active Break** (5-10 mins): Movement, hydration, reset
        - **Optional Round 2**: If energy allows, another focused block

        ⚡ **Focus Techniques Menu:**
        Choose what feels right today:
        - 🎵 Focus music or brown noise
        - 🍅 Visual timer (seeing time helps ADHD brains)
        - 📱 Phone in another room
        - 🎯 "One thing only" mantra
        - 🤝 Body doubling (virtual or in-person)

        🏠 **Environment Setup:**
        - Comfortable temperature
        - Good lighting
        - Fidget tools available
        - Water and snacks nearby
        - Backup task ready (if main task feels impossible)

        💪 **Motivation Boosters:**
        - Start with the most interesting part
        - Set a "minimum viable progress" goal
        - Reward yourself after the session
        - Remember: ANY progress counts!

        🚨 **If Focus Breaks:**
        - No judgment! ADHD brains work differently
        - Gently redirect attention back
        - Take a micro-break if needed
        - Switch to backup task if original feels overwhelming
        """
    
    def _calculate_optimal_duration(self, context: Dict[str, Any], requested_duration: int = None) -> int:
        """Calculate optimal focus duration based on current state."""
        
        if not context:
            return requested_duration or 25
        
        energy_level = context.get("energy_level", 5)
        distraction_level = context.get("distraction_level", 5)
        mood_score = context.get("mood_score", 5)
        
        # Base duration on energy and current state
        if energy_level >= 8 and distraction_level <= 3 and mood_score >= 7:
            optimal_duration = 35  # High capacity day
        elif energy_level >= 6 and distraction_level <= 5:
            optimal_duration = 25  # Standard Pomodoro
        elif energy_level >= 4:
            optimal_duration = 20  # Shorter but doable
        else:
            optimal_duration = 15  # Low energy, gentle approach
        
        # If user requested specific duration, blend with optimal
        if requested_duration:
            return min(requested_duration, optimal_duration + 10)
        
        return optimal_duration
    
    def _generate_break_schedule(self, result: Dict) -> List[Dict[str, Any]]:
        """Generate adaptive break schedule."""
        
        breaks = [
            {
                "after_minutes": 15,
                "type": "micro_break",
                "duration": 2,
                "activities": ["Stretch arms", "Deep breath", "Look away from screen"]
            },
            {
                "after_minutes": 25,
                "type": "active_break", 
                "duration": 5,
                "activities": ["Walk around", "Drink water", "Quick snack", "Light stretching"]
            },
            {
                "after_minutes": 50,
                "type": "reset_break",
                "duration": 10,
                "activities": ["Step outside", "Complete rest from task", "Movement", "Mindfulness"]
            }
        ]
        
        return breaks
    
    def _suggest_focus_techniques(self, task: str, context: Dict[str, Any]) -> List[str]:
        """Suggest focus techniques based on task and context."""
        
        techniques = []
        
        # Base techniques for ADHD
        techniques.extend([
            "🍅 Pomodoro timer with visual countdown",
            "🎵 Focus music or white noise",
            "📱 Phone in airplane mode or another room"
        ])
        
        # Task-specific techniques
        task_lower = task.lower()
        if any(word in task_lower for word in ["write", "creative", "design"]):
            techniques.append("🧠 Brain dump first to clear mental clutter")
        
        if any(word in task_lower for word in ["read", "study", "research"]):
            techniques.append("📝 Active reading with notes or highlights")
        
        if any(word in task_lower for word in ["boring", "admin", "routine"]):
            techniques.extend([
                "🎵 Upbeat music to increase dopamine",
                "🏆 Extra rewards for completion"
            ])
        
        # Context-based techniques
        if context and context.get("distraction_level", 0) >= 7:
            techniques.extend([
                "🔇 Noise-canceling headphones",
                "🚪 Closed door or 'do not disturb' sign"
            ])
        
        return techniques[:5]  # Limit to avoid overwhelm
    
    def _get_environment_suggestions(self, context: Dict[str, Any]) -> List[str]:
        """Get environment optimization suggestions."""
        
        suggestions = [
            "💡 Ensure good lighting (natural light preferred)",
            "🌡️ Comfortable temperature (not too warm)",
            "🧘 Clear, organized workspace",
            "💧 Water bottle within reach",
            "🎯 Only task-relevant items visible"
        ]
        
        if context and context.get("distraction_level", 0) >= 6:
            suggestions.extend([
                "🔇 Use noise-blocking or white noise",
                "📵 All notifications turned off",
                "🚪 Physical barrier from distractions"
            ])
        
        return suggestions
    
    def _generate_suggestions(self) -> List[str]:
        """Generate focus-specific follow-up suggestions."""
        return [
            "How did that focus session feel? Any adjustments needed?",
            "Would you like to try a different focus technique next time?",
            "Should we adjust the session length for your energy level?",
            "Need help setting up your environment for better focus?",
            "Want to try body doubling or accountability for your next session?"
        ]
