import json
from backend.crew.agents.orchestrator import OrchestratorAgent


class DummyLLM:
    def invoke(self, prompt: str) -> str:
        return "dummy response"


def test_orchestrator_context_storage():
    agent = OrchestratorAgent(llm=DummyLLM())
    result = agent.orchestrate_response(
        "How can I focus?",
        context={"mood_score": 5},
        agent_insights={"planning": "Plan your day"},
    )
    assert "response" in result
    assert agent.user_context.get("mood_score") == 5
    assert len(agent.conversation_history) == 1

    result2 = agent.orchestrate_response("Another question", agent_insights={})
    assert len(agent.conversation_history) == 2
