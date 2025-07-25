# AGENTS.md

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


## Development Tasks

Below is the current development plan. Each agent should focus on the tasks in their section.

### LeadPlanner
- Keep `ROADMAP.md` up to date and break milestones 11–13 into actionable tasks.
- Provide time estimates, dependencies, and priority ordering for the remaining work.
- Assess integration gaps between backend and frontend services.
- Document follow-up items for BackendArchitect and FrontendArchitect to close those gaps.

### BackendDeveloper
- Integrate Redis via `REDIS_URL` to persist conversation history.
- Support the CI/CD pipeline with IntegrationEngineer.
- Keep tests up to date for new features.

### FrontendDeveloper
- Display Redis-backed conversation history in the UI.
- Collaborate on the CI/CD pipeline so the React build deploys automatically.
- Handle errors from new endpoints and general network issues.
### BackendArchitect
- Plan Redis caching strategy and database migrations for conversation history.

### FrontendArchitect
- Ensure accessibility and performance standards for the updated UI.
### QATester
- Verify Redis integration by testing cached conversation history.

### IntegrationEngineer
- Build GitHub Actions for linting, tests, and Docker image creation.
- Configure automatic deployment to a staging environment.
- Coordinate environment variables and Docker configuration across services.
### DocsWriter
- Document Redis setup and caching benefits.
- Update CI/CD documentation once the pipeline is live.
