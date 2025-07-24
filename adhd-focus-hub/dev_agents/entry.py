"""Entry point for loading development workflow agents with Codex."""

from . import (
    BackendArchitect,
    FrontendArchitect,
    BackendDeveloper,
    FrontendDeveloper,
    TestingEngineer,
    IntegrationEngineer,
    ProjectManager,
)


def load() -> dict:
    """Return instantiated agents for Codex."""
    return {
        "backend_architect": BackendArchitect(),
        "frontend_architect": FrontendArchitect(),
        "backend_developer": BackendDeveloper(),
        "frontend_developer": FrontendDeveloper(),
        "testing_engineer": TestingEngineer(),
        "integration_engineer": IntegrationEngineer(),
        "project_manager": ProjectManager(),
    }


if __name__ == "__main__":
    agents = load()
    for name, agent in agents.items():
        print(f"Loaded {name}: {agent.role}")
