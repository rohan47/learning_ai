"""Main CrewAI orchestrator for ADHD Focus Hub."""

from typing import Dict, Any, List, Optional
import json
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

from crewai import Crew, Process, LLM
from crewai.project import CrewBase

from .agents import (
    PlanningAgent,
    FocusCoachAgent,
    EmotionalSupportAgent,
    OrganizationAgent,
    LearningAgent,
    OrchestratorAgent
)

# Load environment variables
load_dotenv()


class ADHDFocusHubCrew:
    """ADHD Focus Hub CrewAI implementation."""

    def __init__(self, max_history: Optional[int] = None):
        """Initialize the crew with all ADHD support agents."""
        # Configure Perplexity LLM
        self.llm = LLM(
            model=os.getenv("OPENAI_MODEL", "llama-3.1-sonar-small-128k-online"),
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.perplexity.ai")
        )
        
        self.planning_agent = PlanningAgent(llm=self.llm)
        self.focus_agent = FocusCoachAgent(llm=self.llm)
        self.emotion_agent = EmotionalSupportAgent(llm=self.llm)
        self.organize_agent = OrganizationAgent(llm=self.llm)
        self.learning_agent = LearningAgent(llm=self.llm)
        self.orchestrator_agent = OrchestratorAgent(llm=self.llm)
        
        self.agents = {
            "planning": self.planning_agent,
            "focus": self.focus_agent,
            "emotion": self.emotion_agent,
            "organize": self.organize_agent,
            "learning": self.learning_agent,
            "orchestrator": self.orchestrator_agent
        }
        
        self.max_history = max_history or int(os.getenv("CREW_MAX_HISTORY", "50"))
        self.conversation_history: List[Dict[str, Any]] = []

    def _trim_history(self) -> None:
        """Trim conversation history to the max allowed length."""
        if self.max_history and len(self.conversation_history) > self.max_history:
            excess = len(self.conversation_history) - self.max_history
            self.conversation_history = self.conversation_history[excess:]
    
    def route_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Intelligent routing to appropriate agent(s)."""
        
        # Analyze input to determine which agent(s) to engage
        routing_analysis = self._analyze_routing(user_input, context)
        
        primary_agent = routing_analysis["primary_agent"]
        secondary_agents = routing_analysis.get("secondary_agents", [])
        
        # Execute with primary agent
        primary_result = self._execute_with_agent(
            primary_agent, user_input, context
        )
        
        # Add input from secondary agents if needed
        secondary_insights = []
        for agent_name in secondary_agents:
            if agent_name != primary_agent and agent_name in self.agents:
                secondary_result = self._execute_with_agent(
                    agent_name, user_input, context, is_secondary=True
                )
                secondary_insights.append({
                    "agent": agent_name,
                    "insight": secondary_result.get("response", "")[:200]  # Brief insight
                })
        
        # Combine results
        final_result = {
            "response": primary_result["response"],
            "primary_agent": primary_agent,
            "secondary_insights": secondary_insights,
            "confidence": primary_result.get("confidence", 0.8),
            "suggestions": primary_result.get("suggestions", []),
            "metadata": {
                "routing_reasoning": routing_analysis["reasoning"],
                "agents_consulted": [primary_agent] + secondary_agents,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        # Store in conversation history
        self.conversation_history.append({
            "input": user_input,
            "output": final_result,
            "timestamp": datetime.utcnow().isoformat()
        })
        self._trim_history()
        
        return final_result
    
    def comprehensive_consultation(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Provide comprehensive consultation using orchestrator with all agents."""
        
        # Determine which agents should be consulted based on the request
        consultation_agents = self._determine_consultation_agents(user_input, context)
        
        # Gather insights from relevant agents
        agent_insights = {}
        for agent_name in consultation_agents:
            if agent_name in self.agents and agent_name != "orchestrator":
                try:
                    agent_result = self._execute_with_agent(
                        agent_name, user_input, context, is_secondary=False
                    )
                    agent_insights[agent_name] = agent_result.get("response", "")
                except Exception as e:
                    agent_insights[agent_name] = f"Unable to consult {agent_name} specialist: {str(e)}"
        
        # Use orchestrator to synthesize insights
        try:
            orchestrator_result = self.orchestrator_agent.orchestrate_response(
                user_input, context, agent_insights
            )
            
            # Enhance result with consultation metadata
            orchestrator_result["metadata"].update({
                "consultation_type": "comprehensive",
                "total_agents_consulted": len(agent_insights),
                "consultation_agents": list(agent_insights.keys()),
                "orchestrator_confidence": orchestrator_result.get("confidence", 0.95)
            })
            
            # Store in conversation history
            self.conversation_history.append({
                "input": user_input,
                "output": orchestrator_result,
                "timestamp": datetime.utcnow().isoformat(),
                "consultation_type": "comprehensive"
            })
            self._trim_history()
            
            return orchestrator_result
            
        except Exception as e:
            # Fallback to regular routing if orchestrator fails
            return self.route_request(user_input, context)
    
    def _determine_consultation_agents(self, user_input: str, context: Dict[str, Any] = None) -> List[str]:
        """Determine which agents should be consulted for comprehensive response."""
        
        input_lower = user_input.lower()
        consultation_agents = []
        
        # Always include core agents for comprehensive consultation
        core_keywords = {
            "planning": ["task", "plan", "goal", "time", "schedule", "priority", "organize task"],
            "focus": ["focus", "attention", "concentrate", "distracted", "hyperfocus"],
            "emotion": ["feel", "mood", "stress", "anxious", "overwhelmed", "motivation"],
            "organize": ["organize", "clutter", "space", "mess", "tidy", "environment"],
            "learning": ["learn", "study", "understand", "skill", "practice", "remember"]
        }
        
        # Check for broad/complex requests that benefit from multiple perspectives
        complex_indicators = [
            "help me", "struggling", "overwhelmed", "don't know", "confused",
            "multiple", "everything", "life", "daily", "routine", "system",
            "improve", "better", "change", "start", "begin"
        ]
        
        has_complex_indicators = any(indicator in input_lower for indicator in complex_indicators)
        
        # If it's a complex request, consult all relevant agents
        if has_complex_indicators or len(input_lower.split()) > 10:
            for agent_name, keywords in core_keywords.items():
                if any(keyword in input_lower for keyword in keywords):
                    consultation_agents.append(agent_name)
            
            # If no specific keywords match but it's complex, consult core agents
            if not consultation_agents:
                consultation_agents = ["planning", "emotion", "focus"]
        else:
            # For specific requests, identify top 2-3 relevant agents
            agent_scores = {}
            for agent_name, keywords in core_keywords.items():
                score = sum(1 for keyword in keywords if keyword in input_lower)
                if score > 0:
                    agent_scores[agent_name] = score
            
            # Get top scoring agents
            sorted_agents = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)
            consultation_agents = [agent for agent, score in sorted_agents[:3]]
        
        # Ensure we always have at least one agent to consult
        if not consultation_agents:
            consultation_agents = ["planning"]  # Default fallback
        
        return consultation_agents
    
    def _analyze_routing(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze user input to determine appropriate agent routing."""
        
        input_lower = user_input.lower()
        
        # Keyword analysis for routing with stronger weights for explicit requests
        routing_keywords = {
            "planning": [
                "task", "plan", "schedule", "break down", "priority", "prioritize",
                "time estimate", "time", "deadline", "goal", "project", "todo", 
                "procrastinating", "steps", "organize task", "how long"
            ],
            "focus": [
                "focus", "concentrate", "distracted", "attention", "pomodoro",
                "work session", "hyperfocus", "can't focus", "concentration"
            ],
            "emotion": [
                "feel", "mood", "overwhelmed", "anxious", "frustrated", "motivation",
                "depressed", "stressed", "rejection", "shame", "tired", "energy"
            ],
            "organize": [
                "organize space", "clutter", "mess", "tidy", "space", "room", "desk",
                "papers", "files", "storage", "clean", "declutter", "organize my"
            ],
            "learning": [
                "learn", "study", "understand", "remember", "memorize", "research",
                "course", "education", "knowledge", "skill", "practice"
            ]
        }
        
        # Score each agent based on keyword matches with stronger weights for explicit terms
        agent_scores = {}
        for agent_name, keywords in routing_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in input_lower:
                    # Give higher weight to explicit, longer phrases
                    weight = len(keyword.split()) * 2 if len(keyword.split()) > 1 else 1
                    score += weight
            agent_scores[agent_name] = score
        
        # Context-based adjustments
        if context:
            mood_score = context.get("mood_score", 5)
            energy_level = context.get("energy_level", 5)
            
            # Low mood/energy might benefit from emotional support
            if mood_score <= 3 or energy_level <= 3:
                agent_scores["emotion"] += 2
            
            # High stress might need organization or emotional support
            stress_level = context.get("stress_level", 5)
            if stress_level >= 7:
                agent_scores["emotion"] += 1
                agent_scores["organize"] += 1
        
        # Recent conversation context - reduce impact to prevent sticky routing
        if self.conversation_history:
            recent_agent = self.conversation_history[-1]["output"]["primary_agent"]
            # Much smaller bonus for continuity to prevent routing conflicts
            if recent_agent in agent_scores:
                agent_scores[recent_agent] += 0.1  # Reduced from 0.5
        
        # Determine primary and secondary agents
        sorted_agents = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)
        
        primary_agent = sorted_agents[0][0] if sorted_agents[0][1] > 0 else "emotion"
        
        # Secondary agents (if close scores or specific patterns)
        secondary_agents = []
        if len(sorted_agents) > 1 and sorted_agents[1][1] >= sorted_agents[0][1] - 1:
            secondary_agents.append(sorted_agents[1][0])
        
        # Special multi-agent scenarios
        if "overwhelmed" in input_lower:
            secondary_agents.extend(["emotion", "planning", "organize"])
        if "can't focus" in input_lower and "messy" in input_lower:
            secondary_agents.extend(["focus", "organize"])
        
        # Remove duplicates and primary from secondary
        secondary_agents = list(set(secondary_agents))
        if primary_agent in secondary_agents:
            secondary_agents.remove(primary_agent)
        
        reasoning = f"Primary: {primary_agent} (score: {agent_scores[primary_agent]})"
        if secondary_agents:
            reasoning += f", Secondary: {', '.join(secondary_agents)}"
        
        return {
            "primary_agent": primary_agent,
            "secondary_agents": secondary_agents[:2],  # Limit to 2 secondary
            "reasoning": reasoning,
            "all_scores": agent_scores
        }
    
    def _execute_with_agent(
        self, 
        agent_name: str, 
        user_input: str, 
        context: Dict[str, Any] = None,
        is_secondary: bool = False
    ) -> Dict[str, Any]:
        """Execute request with specific agent."""
        
        if agent_name not in self.agents:
            return {
                "response": f"Agent {agent_name} not available",
                "confidence": 0.0
            }
        
        agent = self.agents[agent_name]
        
        # Add timestamp to input to prevent caching issues
        timestamped_input = f"{user_input} [Request at {datetime.utcnow().isoformat()}]"
        
        # For secondary agents, modify the request to be brief
        if is_secondary:
            modified_input = f"Brief insight on: {timestamped_input}"
            return agent.execute_with_context(modified_input, context)
        else:
            return agent.execute_with_context(timestamped_input, context)
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        
        status = {
            "total_agents": len(self.agents),
            "agents": {},
            "total_conversations": len(self.conversation_history),
            "system_uptime": datetime.utcnow().isoformat()
        }
        
        for agent_name, agent in self.agents.items():
            status["agents"][agent_name] = {
                "role": agent.role,
                "total_interactions": len(getattr(agent, 'conversation_history', [])),
                "available": True
            }
        
        return status
    
    def get_conversation_summary(self, limit: int = 10) -> Dict[str, Any]:
        """Get recent conversation summary."""
        
        recent_conversations = self.conversation_history[-limit:] if self.conversation_history else []
        
        agent_usage = {}
        for conv in recent_conversations:
            primary_agent = conv["output"]["primary_agent"]
            agent_usage[primary_agent] = agent_usage.get(primary_agent, 0) + 1
        
        return {
            "recent_conversations": len(recent_conversations),
            "agent_usage": agent_usage,
            "most_used_agent": max(agent_usage, key=agent_usage.get) if agent_usage else None,
            "conversations": [
                {
                    "input": conv["input"][:100] + "..." if len(conv["input"]) > 100 else conv["input"],
                    "primary_agent": conv["output"]["primary_agent"],
                    "timestamp": conv["timestamp"]
                }
                for conv in recent_conversations
            ]
        }
    
    async def async_route_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Async version of route_request for FastAPI integration."""
        
        # Run the synchronous routing in a thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, self.route_request, user_input, context
        )
        return result
    
    def clear_conversation_history(self) -> None:
        """Clear conversation history to prevent routing conflicts."""
        self.conversation_history = []
        
        # Also clear any agent-specific conversation history
        for agent in self.agents.values():
            if hasattr(agent, 'conversation_history'):
                agent.conversation_history = []
    
    def force_agent_refresh(self) -> None:
        """Force refresh of all agents to clear any cached state."""
        # Reinitialize agents to clear any cached responses
        self.planning_agent = PlanningAgent(llm=self.llm)
        self.focus_agent = FocusCoachAgent(llm=self.llm)
        self.emotion_agent = EmotionalSupportAgent(llm=self.llm)
        self.organize_agent = OrganizationAgent(llm=self.llm)
        self.learning_agent = LearningAgent(llm=self.llm)
        self.orchestrator_agent = OrchestratorAgent(llm=self.llm)
        
        self.agents = {
            "planning": self.planning_agent,
            "focus": self.focus_agent,
            "emotion": self.emotion_agent,
            "organize": self.organize_agent,
            "learning": self.learning_agent,
            "orchestrator": self.orchestrator_agent
        }
        
        self.conversation_history = []
