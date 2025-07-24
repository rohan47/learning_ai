"""Base class for development workflow agents."""

from crewai import Agent
from typing import Dict, Any, List
from datetime import datetime


class BaseDevAgent:
    """General-purpose agent with simple context tracking."""

    def __init__(self, role: str, goal: str, backstory: str, tools: List = None, llm=None, **kwargs):
        # Underlying CrewAI agent
        self.agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools or [],
            verbose=True,
            allow_delegation=False,
            llm=llm,
            **kwargs,
        )

        self.conversation_history: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}

        self.role = self.agent.role
        self.goal = self.agent.goal
        self.backstory = self.agent.backstory

    def execute_with_context(self, task_description: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Execute a task using stored context."""
        if context:
            self.context.update(context)

        prompt = self._build_contextual_prompt(task_description, self.context)
        response = self._process_request(prompt)

        result = {
            "agent": self.role,
            "response": response,
            "context_used": self.context,
            "timestamp": datetime.utcnow().isoformat(),
        }

        self.conversation_history.append({
            "input": task_description,
            "output": result,
            "timestamp": datetime.utcnow().isoformat(),
        })
        return result

    def _build_contextual_prompt(self, task: str, context: Dict[str, Any]) -> str:
        prompt_parts = [f"Task: {task}", "", "Context:"]
        for key, value in context.items():
            prompt_parts.append(f"- {key}: {value}")
        if self.conversation_history:
            recent = self.conversation_history[-1]
            prompt_parts.append(f"- Recent interaction: {recent['input'][:100]}...")
        prompt_parts.append("\nProvide guidance to complete the task.")
        return "\n".join(prompt_parts)

    def _process_request(self, prompt: str) -> str:
        """Placeholder processing method."""
        return f"[{self.role}] {prompt[:100]}"

    def get_specialized_tools(self) -> List:
        """Return tools specific to this agent."""
        return []
