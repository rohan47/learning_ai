"""Base ADHD Agent with common functionality."""

from crewai import Agent
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json
from datetime import datetime


class BaseADHDAgent:
    """Base class for all ADHD support agents with common functionality."""
    
    def __init__(self, role: str, goal: str, backstory: str, tools: List = None, llm=None, **kwargs):
        # Create the underlying CrewAI agent
        self.agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools or [],
            verbose=True,
            allow_delegation=False,
            llm=llm,
            **kwargs
        )
        
        # Add ADHD-specific attributes
        self.conversation_history = []
        self.user_context = {}
        
        # Expose agent properties
        self.role = self.agent.role
        self.goal = self.agent.goal
        self.backstory = self.agent.backstory
    
    def execute_with_context(
        self, 
        task_description: str, 
        context: Dict[str, Any] = None, 
        expected_output: str = None
    ) -> Dict[str, Any]:
        """Execute agent task with ADHD-specific context awareness."""
        
        # Store context for this session
        if context:
            self.user_context.update(context)
        
        # Build contextual prompt
        contextual_prompt = self._build_contextual_prompt(
            task_description, 
            self.user_context
        )
        
        # Execute the task (this would integrate with CrewAI's execution engine)
        result = {
            "agent": self.role,
            "response": self._process_request(contextual_prompt),
            "context_used": self.user_context,
            "timestamp": datetime.utcnow().isoformat(),
            "confidence": self._calculate_confidence(),
            "suggestions": self._generate_suggestions()
        }
        
        # Store in conversation history
        self.conversation_history.append({
            "input": task_description,
            "output": result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return result
    
    def _build_contextual_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """Build an ADHD-aware contextual prompt."""
        
        prompt_parts = [
            f"Task: {task}",
            "",
            "ADHD Context Considerations:",
        ]
        
        # Add time of day context for energy levels
        current_hour = datetime.now().hour
        if 6 <= current_hour < 12:
            prompt_parts.append("- Morning: Higher energy, better for complex tasks")
        elif 12 <= current_hour < 17:
            prompt_parts.append("- Afternoon: Moderate energy, good for routine tasks")
        else:
            prompt_parts.append("- Evening: Lower energy, better for creative/reflective tasks")
        
        # Add user-specific context
        if context.get("mood_score"):
            mood = context["mood_score"]
            if mood <= 3:
                prompt_parts.append(f"- User mood is low ({mood}/10): Provide extra support and encouragement")
            elif mood >= 8:
                prompt_parts.append(f"- User mood is high ({mood}/10): User may be energetic, can handle more challenging tasks")
        
        if context.get("energy_level"):
            energy = context["energy_level"]
            if energy <= 3:
                prompt_parts.append(f"- Low energy ({energy}/10): Suggest shorter tasks and frequent breaks")
            elif energy >= 8:
                prompt_parts.append(f"- High energy ({energy}/10): User can tackle demanding tasks")
        
        if context.get("distraction_level"):
            distraction = context["distraction_level"]
            if distraction >= 7:
                prompt_parts.append(f"- High distraction environment ({distraction}/10): Suggest focus techniques and environmental changes")
        
        # Add recent context
        if self.conversation_history:
            recent = self.conversation_history[-1]
            prompt_parts.append(f"- Recent interaction: {recent['input'][:100]}...")
        
        prompt_parts.extend([
            "",
            "Response Guidelines:",
            "- Be encouraging and non-judgmental",
            "- Provide specific, actionable steps",
            "- Consider executive dysfunction challenges",
            "- Include time estimates with buffer time",
            "- Acknowledge ADHD-specific difficulties",
            "- Offer alternatives if first approach doesn't work",
            "",
            "Please provide a response that addresses the task while being mindful of these ADHD considerations."
        ])
        
        return "\n".join(prompt_parts)
    
    def _process_request(self, prompt: str) -> str:
        """Process the request - to be implemented by specific agents."""
        # This would typically call the LLM with the agent's specific expertise
        # For now, return a placeholder that would be replaced with actual LLM call
        return f"[{self.role}] Processing: {prompt[:100]}..."
    
    def _calculate_confidence(self) -> float:
        """Calculate confidence score for the response."""
        # Base confidence on context completeness and agent expertise
        base_confidence = 0.8
        
        # Increase confidence if we have user context
        if self.user_context:
            base_confidence += 0.1
        
        # Increase confidence if we have conversation history
        if self.conversation_history:
            base_confidence += 0.05
        
        return min(base_confidence, 1.0)
    
    def _generate_suggestions(self) -> List[str]:
        """Generate follow-up suggestions based on agent specialization."""
        # Default suggestions - to be overridden by specific agents
        return [
            "Would you like me to break this down further?",
            "How are you feeling about this approach?",
            "Is there anything specific you'd like me to adjust?"
        ]
    
    @abstractmethod
    def get_specialized_tools(self) -> List:
        """Return tools specific to this agent's specialization."""
        pass
    
    def update_user_context(self, new_context: Dict[str, Any]):
        """Update user context with new information."""
        self.user_context.update(new_context)
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of recent conversations."""
        return {
            "total_interactions": len(self.conversation_history),
            "recent_topics": [h["input"][:50] for h in self.conversation_history[-3:]],
            "user_context": self.user_context,
            "agent_role": self.role
        }
