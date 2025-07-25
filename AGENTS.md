# Development Agents for Codex

This repository uses CrewAI-based development agents located in `adhd-focus-hub/dev_agents/`. They streamline planning, implementation, and testing when working with Codex.

## Agents

| Agent | Role |
|-------|------|
| **LeadPlanner** | Break down features and create a roadmap. |
| **BackendArchitect** | Design scalable backend systems. |
| **FrontendArchitect** | Define frontend component architecture. |
| **BackendDeveloper** | Implement API endpoints, manage database models, maintain authentication logic, and write tests. |
| **FrontendDeveloper** | Build responsive React/TypeScript UIs, handle state management, and integrate with the backend API. |
| **IntegrationEngineer** | Manage CI/CD and service integration. |
| **QATester** | Execute tests and report results. |
| **DocsWriter** | Update project documentation. |

## Usage

Before running any agents, set your `OPENAI_API_KEY` environment variable:
```bash
export OPENAI_API_KEY=your_openai_api_key
```

If the `codex` command is missing, run the helper script to install it:
```bash
./scripts/install_codex.sh
```

Start Codex with any combination of these agents. Example:
```bash
codex agents start LeadPlanner BackendDeveloper FrontendDeveloper QATester DocsWriter
```

The agents are imported from the `adhd_focus_hub.dev_agents` package.

## Development Tasks

Below is the current development plan. Each agent should focus on the tasks in their section.

### LeadPlanner
- Keep `ROADMAP.md` up to date and break milestones 1&ndash;6 into actionable tasks.
- Provide time estimates, dependencies, and priority ordering for the remaining work.
- Assess integration gaps between backend and frontend services.
- Document follow-up items for BackendArchitect and FrontendArchitect to close those gaps.

### BackendDeveloper
- Create Docker compose files and scripts for backend deployment.
- Audit API endpoints against React services and fix any mismatched routes.
- Implement `/api/v1/organize` and `/api/v1/learn` endpoints with tests.
- Integrate Redis via `REDIS_URL` to persist conversation history.
- Run `python adhd-focus-hub/test_tools.py` after making changes.

### FrontendDeveloper
- Add services and UI components for the organization and learning endpoints.
- Display Redis-backed conversation history in the UI.
- Collaborate on the CI/CD pipeline so the React build deploys automatically.
- Handle errors from new endpoints and general network issues.

### BackendArchitect
- Design Docker-based deployment architecture for backend and frontend services.
- Publish the updated API contract during frontend–backend alignment.
- Plan Redis caching strategy and database migrations for conversation history.

### FrontendArchitect
- Outline component patterns for organization and learning features.
- Ensure accessibility and performance standards for the updated UI.
- Coordinate with BackendArchitect to finalize API paths and types.

### QATester
- Add tests for `/api/v1/organize` and `/api/v1/learn` endpoints.
- Verify Redis integration by testing cached conversation history.
- Confirm the repository includes a `LICENSE` file referenced in `README.md`.
- Ensure CI runs the test suite on each pull request.

### IntegrationEngineer
- Build GitHub Actions for linting, tests, and Docker image creation.
- Configure automatic deployment to a staging environment.
- Coordinate environment variables and Docker configuration across services.

### DocsWriter
- Document Docker deployment steps and container registry usage.
- Update API documentation after frontend–backend alignment.
- Describe the organization and learning features with example requests.
- Explain Redis setup and caching benefits.
- Reference the MIT `LICENSE` in `README.md` and other docs.
- Note how to run `python adhd-focus-hub/test_tools.py` as part of development.

