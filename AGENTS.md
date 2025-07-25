# Development Agents for Codex

This repository uses CrewAI-based development agents located in `adhd-focus-hub/dev_agents/`. They streamline planning, implementation, and testing when working with Codex.

## Agents

| Agent | Role |
|-------|------|
| **LeadPlanner** | Break down features and create a roadmap. |
| **BackendArchitect** | Design scalable backend systems. |
| **FrontendArchitect** | Define frontend component architecture. |
| **BackendDeveloper** | Work on the FastAPI backend. |
| **FrontendDeveloper** | Implement the React/TypeScript frontend. |
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
- Turn the "Next Steps" section in `PROJECT_STATUS.md` into sequential milestones: environment setup, CrewAI tool fixes, database layer, authentication, frontend integration, comprehensive testing, and deployment.
- Break each milestone into discrete tasks with clear deliverables and success criteria.
- Provide time estimates and priority ordering for the remaining work.
- Assess integration gaps between the backend and React frontend.
- Document tasks for BackendArchitect and FrontendArchitect to address the gaps.

### BackendDeveloper
- Create `backend/.env.example` with `OPENAI_API_KEY`, `DATABASE_URL`, `REDIS_URL`, and `SECRET_KEY`.
- Ensure `load_dotenv()` in `backend/api/main.py` loads a local `.env` file.
- Review `backend/crew/tools/` for Pydantic v2 compliance and update models if necessary.
- Implement SQLAlchemy models (User, Task, MoodLog) with Alembic migrations and connect to PostgreSQL via `DATABASE_URL`.
- Add JWT-based authentication and protect API routes with `HTTPBearer`.
- Create CRUD endpoints for tasks and mood logs.
- Run `python adhd-focus-hub/test_tools.py` after making changes.

### FrontendDeveloper
- Add login and registration pages that store JWT tokens securely.
- Update service files in `frontend/src/services/` to call the new authentication and CRUD endpoints with the token.
- Connect existing pages so they fetch and save real data from the backend.
- Provide graceful error handling for authentication failures or network issues.

### BackendArchitect
- Review database schemas and API design for scalability.
- Propose deployment architecture and security best practices.
- Resolve API route mismatches with the frontend and publish a clear contract.

### FrontendArchitect
- Define the component hierarchy and shared state patterns.
- Establish accessibility and performance standards for UI.
- Review service APIs against backend routes and update types or paths to match.

### QATester
- Expand `adhd-focus-hub/test_tools.py` into a pytest suite covering planning tools and all API endpoints (authentication, tasks, mood logs).
- Write tests for token validation, database CRUD operations, and error conditions.
- Document how to run the tests and ensure the results are shared in pull requests.

### IntegrationEngineer
- Maintain CI/CD pipelines and ensure backend and frontend build correctly.
- Coordinate environment variables and Docker configuration across services.

### DocsWriter
- Update `README.md` with setup instructions for `.env.example`, database initialization, and running backend and frontend services.
- Document new authentication routes and CRUD endpoints with example requests.
- Describe the testing process and how development agents should run `python adhd-focus-hub/test_tools.py`.
- Provide a brief guide on using the development agents defined in this file.

