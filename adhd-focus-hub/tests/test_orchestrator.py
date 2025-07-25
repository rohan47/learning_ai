import json
import pytest
from backend.crew.agents.orchestrator import OrchestratorAgent
from backend.crew.exceptions import LLMUnavailableError


class DummyLLM:
    def call(self, prompt: str) -> str:
        return "dummy response"


def test_orchestrator_context_storage():
    agent = OrchestratorAgent(llm=DummyLLM())
    with pytest.raises(LLMUnavailableError):
        agent.orchestrate_response(
            "How can I focus?",
            context={"mood_score": 5},
            agent_insights={"planning": "Plan your day"},
        )
