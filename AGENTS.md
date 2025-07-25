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
- Keep `ROADMAP.md` up to date and break milestones 1&ndash;6 into actionable tasks.
- Provide time estimates, dependencies, and priority ordering for the remaining work.
- Assess integration gaps between backend and frontend services.
- Document follow-up items for BackendArchitect and FrontendArchitect to close those gaps.

### BackendDeveloper
- Create Docker compose files and scripts for backend deployment.
- Audit API endpoints against React services and fix any mismatched routes.
- Implement `/api/v1/organize` and `/api/v1/learn` endpoints with tests.
- Integrate Redis via `REDIS_URL` to persist conversation history.

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

### IntegrationEngineer
- Build GitHub Actions for linting, tests, and Docker image creation.
- Configure automatic deployment to a staging environment.
- Coordinate environment variables and Docker configuration across services.

### DocsWriter
- Document Docker deployment steps and container registry usage.
- Update API documentation after frontend–backend alignment.
- Describe the organization and learning features with example requests.
- Explain Redis setup and caching benefits.


