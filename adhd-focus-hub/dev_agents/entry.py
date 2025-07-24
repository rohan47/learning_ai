"""Entry point for loading development workflow agents with Codex."""

from . import (
    BackendDeveloper,
    FrontendDeveloper,
    LeadPlanner,
    QATester,
    DocsWriter,
)


def load() -> dict:
    """Return instantiated agents for Codex."""
    return {
        "lead_planner": LeadPlanner(),
        "backend_developer": BackendDeveloper(),
        "frontend_developer": FrontendDeveloper(),
        "qa_tester": QATester(),
        "docs_writer": DocsWriter(),
    }


if __name__ == "__main__":
    agents = load()
    for name, agent in agents.items():
        print(f"Loaded {name}: {agent.role}")
