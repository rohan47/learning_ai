"""Main Orchestrator Agent for ADHD Focus Hub."""

from typing import Dict, Any, List
from datetime import datetime
from crewai import LLM

from .base import BaseADHDAgent


class OrchestratorAgent(BaseADHDAgent):
    """Main orchestrator agent that consults with all specialized ADHD agents."""

    def __init__(self, llm: LLM):
        """Initialize the orchestrator agent."""
        super().__init__(
            role="ADHD Support Orchestrator",
            goal="Coordinate multiple ADHD specialists to provide comprehensive support",
            backstory="""You are the main ADHD support coordinator who works with a team of specialized agents.
        Your role is to understand user needs, consult with the appropriate specialists, and synthesize their insights
        into comprehensive, actionable advice. You have access to planning, focus, emotional support, organization,
        and learning specialists.""",
            llm=llm,
        )
        self.llm = llm
    
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
            result = self.execute_with_context(orchestrator_prompt, context or {})

            raw_response = result["response"]
            formatted = self._format_orchestrator_response(raw_response, agent_insights)

            questions = self._generate_clarifying_questions(context)
            result.update({
                "response": formatted,
                "suggestions": self._extract_suggestions(raw_response, context),
                "clarifying_questions": questions,
                "consultation_summary": self._create_consultation_summary(agent_insights),
            })

            metadata = result.get("metadata", {})
            metadata.update({
                "orchestrator_used": True,
                "agents_consulted": list(agent_insights.keys()) if agent_insights else [],
                "consultation_timestamp": datetime.utcnow().isoformat(),
            })
            result["metadata"] = metadata

            return result
            
        except Exception as e:
            return {
                "response": "I'm having trouble coordinating with my specialist team right now. Let me provide basic guidance based on your request.",
                "confidence": 0.3,
                "suggestions": ["Try asking a more specific question", "Check if the backend is fully operational"],
                "error": str(e)
            }
    
    
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

    def _process_request(self, prompt: str) -> str:
        """Process the orchestrator prompt using the LLM."""
        try:
            response = self.llm.invoke(prompt)
            return str(response)
        except Exception:
            return (
                "I understand you need comprehensive ADHD support. "
                "Based on your request, let me provide guidance across multiple areas that may help."
            )
    
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
    
    def _extract_suggestions(self, response: str, context: Dict[str, Any] = None) -> List[str]:
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
        
        clarifying = self._generate_clarifying_questions(context)
        suggestions.extend(clarifying)

        # Limit length but ensure clarifying questions are included
        max_len = max(4, len(suggestions))
        return suggestions[:max_len]
    
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

    def _generate_clarifying_questions(self, context: Dict[str, Any] = None) -> List[str]:
        """Generate clarifying questions based on missing context."""

        context = context or {}
        questions = []

        if not context.get("daily_routine"):
            questions.append("What does a typical day look like for you?")
        if not context.get("challenges"):
            questions.append("Which ADHD-related challenges do you struggle with most?")
        if not context.get("strengths"):
            questions.append("Are there strategies that already work well for you?")
        if not context.get("preferences"):
            questions.append("Do you prefer any specific tools or apps to stay organized?")
        if not context.get("existing_strategies"):
            questions.append("What approaches have you tried before to manage your ADHD?")

        return questions

