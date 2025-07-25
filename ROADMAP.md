# Development Roadmap

This document translates the **Next Steps** from `adhd-focus-hub/PROJECT_STATUS.md` into a structured plan for all development agents.

Each milestone is ordered by priority with an estimated time to complete.

| Priority | Milestone | Key Tasks | Deliverables | Success Criteria | Est. Time | Status |
|---------|----------|-----------|--------------|-----------------|-----------|--------|
| 1 | **Orchestrator Alignment** | - Refactor `OrchestratorAgent` to extend `BaseADHDAgent`.<br>- Add context storage and conversation history.<br>- Update crew integration and unit tests. | Unified orchestrator with base features. | Tests confirm orchestration with stored context. | 1 day | ✅ Completed |
| 2 | **Deployment** | - Create Docker compose for backend/frontend.<br>- Document deployment steps.<br>- Push images to container registry. | Dockerfiles and compose config for production. | Application deploys successfully on staging environment. | 1.5 days | ⏳ Pending |
| 3 | **Frontend-Backend Alignment** | - Audit API endpoints and React services.<br>- Resolve route mismatches such as mood logging.<br>- Document the final API contract. | Unified interface between layers. | Frontend calls all endpoints without errors. | 0.5 day | ⏳ Pending |

## Timeline Overview

Milestones 1–6 are complete. Orchestrator alignment, deployment, and frontend-backend alignment remain, totaling approximately **3.0 days** of work. Adjust as necessary based on team availability.

## Usage by Agents

- **BackendDeveloper** focuses on milestones 1–4.
- **FrontendDeveloper** tackles milestones 4–5.
- **QATester** covers milestone 6.
- **DocsWriter** updates documentation across all milestones.
- **BackendArchitect** reviews backend design and guides deployment.
- **FrontendArchitect** defines component architecture and performance standards.
- **IntegrationEngineer** manages CI/CD pipelines for smooth releases.

This roadmap should keep all agents aligned as the project progresses.

## Implemented

| Priority | Milestone | Key Tasks | Deliverables | Success Criteria | Est. Time | Status |
|---------|----------|-----------|--------------|-----------------|-----------|-------|
| 1 | **Environment Setup** | - Create `backend/.env.example` with required variables.<br>- Document local setup in README.<br>- Add real `.env` locally with `OPENAI_API_KEY`. | Sample `.env.example` file and updated docs. | Backend runs with environment variables loaded. | 0.5 day | ✅ Completed |
| 2 | **CrewAI Tool Fixes** | - Review tools in `backend/crew/tools/` for Pydantic v2 issues.<br>- Update models/functions for compatibility.<br>- Run `python adhd-focus-hub/test_tools.py`. | Updated tool code and passing tests. | Test script outputs success for all tools. | 1 day | ✅ Completed |
| 3 | **Database Layer** | - Set up SQLAlchemy models (User, Task, MoodLog).<br>- Configure PostgreSQL via `DATABASE_URL`.<br>- Create Alembic migrations.<br>- Document setup in README. | Database models and migrations committed. | Migrations run without errors and tables created. | 2 days | ✅ Completed |
| 4 | **Authentication** | - Implement JWT-based auth in FastAPI.<br>- Protect endpoints with `HTTPBearer`.<br>- Create login/register routes.<br>- Add token storage in frontend. | Auth API and middleware. | Login and protected routes work with valid tokens. | 2 days | ✅ Completed |
| 5 | **Frontend Integration** | - Update services in `frontend/src/services` to call backend APIs with auth tokens.<br>- Build login and registration pages.<br>- Connect task and mood pages to backend. | Working frontend communicating with backend. | Users can authenticate and CRUD data from UI. | 2 days | ✅ Completed |
| 6 | **Comprehensive Testing** | - Expand `test_tools.py` into pytest suite.<br>- Cover all API endpoints and auth flow.<br>- Add CI instructions. | Pytest tests under `tests/` directory. | Test suite passes locally and in CI. | 1.5 days | ✅ Completed |
