"""Main Orchestrator Agent for ADHD Focus Hub."""

from typing import Dict, Any, List
from datetime import datetime
from crewai import LLM


class OrchestratorAgent:
    """Main orchestrator agent that consults with all specialized ADHD agents."""
    
    def __init__(self, llm: LLM):
        """Initialize the orchestrator agent."""
        self.llm = llm
        self.role = "ADHD Support Orchestrator"
        self.goal = "Coordinate multiple ADHD specialists to provide comprehensive support"
        self.backstory = """You are the main ADHD support coordinator who works with a team of specialized agents. 
        Your role is to understand user needs, consult with the appropriate specialists, and synthesize their insights 
        into comprehensive, actionable advice. You have access to planning, focus, emotional support, organization, 
        and learning specialists."""
    
    def orchestrate_response(
        self, 
        user_input: str, 
        context: Dict[str, Any] = None,
        agent_insights: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Orchestrate a comprehensive response using insights from multiple agents."""
        
        # Build the orchestrator prompt
        orchestrator_prompt = self._build_orchestrator_prompt(user_input, context, agent_insights)
        
        try:
            # Get orchestrator response using LLM directly
            response = self._generate_response(orchestrator_prompt)
            
            # Parse and structure the response
            return {
                "response": self._format_orchestrator_response(response, agent_insights),
                "confidence": 0.95,
                "suggestions": self._extract_suggestions(response),
                "consultation_summary": self._create_consultation_summary(agent_insights),
                "metadata": {
                    "orchestrator_used": True,
                    "agents_consulted": list(agent_insights.keys()) if agent_insights else [],
                    "consultation_timestamp": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "response": "I'm having trouble coordinating with my specialist team right now. Let me provide basic guidance based on your request.",
                "confidence": 0.3,
                "suggestions": ["Try asking a more specific question", "Check if the backend is fully operational"],
                "error": str(e)
            }
    
    def _generate_response(self, prompt: str) -> str:
        """Generate response using the LLM directly."""
        try:
            # Use the LLM to generate a response
            response = self.llm.invoke(prompt)
            return str(response)
        except Exception as e:
            return f"I understand you need comprehensive ADHD support. Based on your request, let me provide guidance across multiple areas that may help."
    
    def _build_orchestrator_prompt(
        self, 
        user_input: str, 
        context: Dict[str, Any] = None,
        agent_insights: Dict[str, str] = None
    ) -> str:
        """Build a comprehensive prompt for the orchestrator."""
        
        prompt = f"""
As the ADHD Support Orchestrator, analyze this user request and provide comprehensive guidance:

USER REQUEST: "{user_input}"

CONTEXT: {context if context else "None provided"}

SPECIALIST CONSULTATIONS:
"""
        
        if agent_insights:
            for agent_name, insight in agent_insights.items():
                prompt += f"""
{agent_name.upper()} SPECIALIST: {insight}
"""
        else:
            prompt += "No specialist consultations available for this request."
        
        prompt += f"""

YOUR TASK:
1. Synthesize the specialist insights into a coherent, comprehensive response
2. Identify any gaps or conflicting advice between specialists
3. Provide practical, ADHD-friendly action steps
4. Consider the user's likely emotional state and energy level
5. Suggest next steps or follow-up actions

RESPONSE FORMAT:
- Start with empathy and validation
- Provide clear, actionable guidance
- Include specific ADHD-friendly strategies
- End with encouragement and next steps

Remember: You're helping someone with ADHD who may be overwhelmed, so be:
- Clear and concise
- Empathetic and non-judgmental
- Practical and specific
- Encouraging and supportive
"""
        
        return prompt
    
    def _format_orchestrator_response(self, response: str, agent_insights: Dict[str, str] = None) -> str:
        """Format the orchestrator response with insights summary."""
        
        formatted_response = f"🧠 **Comprehensive ADHD Support Response**\n\n"
        
        if agent_insights and len(agent_insights) > 0:
            formatted_response += f"📋 **Consultation Process:**\n"
            formatted_response += f"I've consulted with {len(agent_insights)} specialist(s) to provide you with comprehensive guidance:\n\n"
            
            # Show each specialist's insight
            specialist_names = {
                "planning": "📅 Planning Specialist",
                "focus": "🎯 Focus Specialist", 
                "emotion": "💝 Emotional Support Specialist",
                "organize": "📦 Organization Specialist",
                "learning": "📚 Learning Specialist"
            }
            
            for agent_name, insight in agent_insights.items():
                specialist_name = specialist_names.get(agent_name, f"🤖 {agent_name.title()} Specialist")
                # Truncate long insights for readability
                short_insight = insight[:200] + "..." if len(insight) > 200 else insight
                formatted_response += f"**{specialist_name}:**\n{short_insight}\n\n"
            
            formatted_response += f"---\n\n**🎯 Synthesized Guidance:**\n{response}\n\n"
        else:
            formatted_response += f"{response}\n\n"
        
        if agent_insights and len(agent_insights) > 1:
            formatted_response += f"💡 **Multi-Perspective Approach:** This response combines insights from {len(agent_insights)} specialists to address your needs holistically."
        
        return formatted_response
    
    def _extract_suggestions(self, response: str) -> List[str]:
        """Extract actionable suggestions from the response."""
        
        suggestions = [
            "Would you like me to dive deeper into any specific area?",
            "Should we create a step-by-step action plan?",
            "Would you like reminders or check-ins for these strategies?",
            "Do you need help breaking any of these tasks down further?"
        ]
        
        # Try to extract specific suggestions from the response
        if "next step" in response.lower():
            suggestions.insert(0, "Focus on the next immediate step to avoid overwhelm")
        if "schedule" in response.lower() or "time" in response.lower():
            suggestions.insert(0, "Consider setting up reminders or time blocks")
        if "break" in response.lower() or "chunk" in response.lower():
            suggestions.insert(0, "Break large tasks into smaller, manageable pieces")
        
        return suggestions[:4]  # Limit to 4 suggestions
    
    def _create_consultation_summary(self, agent_insights: Dict[str, str] = None) -> Dict[str, Any]:
        """Create a summary of the consultation process."""
        
        if not agent_insights:
            return {"total_consultations": 0, "specialists": [], "insights_preview": {}}
        
        # Create preview of each specialist's contribution
        insights_preview = {}
        for agent_name, insight in agent_insights.items():
            # Get first sentence or first 100 characters as preview
            preview = insight.split('.')[0] + '.' if '.' in insight else insight[:100] + "..."
            insights_preview[agent_name] = preview
        
        return {
            "total_consultations": len(agent_insights),
            "specialists": list(agent_insights.keys()),
            "consultation_depth": "comprehensive" if len(agent_insights) >= 3 else "focused",
            "coverage_areas": self._identify_coverage_areas(agent_insights),
            "insights_preview": insights_preview,
            "consultation_quality": "high" if len(agent_insights) >= 2 else "standard"
        }
    
    def _identify_coverage_areas(self, agent_insights: Dict[str, str]) -> List[str]:
        """Identify what areas were covered in the consultation."""
        
        areas = []
        agent_mapping = {
            "planning": "Task Management & Planning",
            "focus": "Attention & Focus Strategies",
            "emotion": "Emotional Support & Regulation",
            "organize": "Organization & Environment",
            "learning": "Learning & Skill Development"
        }
        
        for agent_name in agent_insights.keys():
            if agent_name in agent_mapping:
                areas.append(agent_mapping[agent_name])
        
        return areas

    def execute_with_context(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute orchestrator with context - compatibility method."""
        return self.orchestrate_response(user_input, context)
