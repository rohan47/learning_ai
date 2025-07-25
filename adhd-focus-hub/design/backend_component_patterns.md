# Backend Component Patterns for Organization and Learning Features

This document outlines recommended FastAPI component patterns that align with the React component guidelines. Following these patterns will keep the backend maintainable and ensure a smooth contract with the frontend.

## 1. API Structure
- Keep route modules grouped by feature under `backend/api/routes/`.
- Expose dedicated endpoints:
  - `POST /api/v1/organize` handled in `routes/organize.py`.
  - `POST /api/v1/learn` handled in `routes/learning.py`.
- Each module should define its router and focus on request validation and response serialization.

## 2. Pydantic Models
- Centralize request and response schemas in `backend/api/models.py`.
- Mirror the fields used by the frontend `services/types.ts` so that types stay in sync.
- Provide clear validation rules and default values to minimize backend errors.

## 3. Service Layer
- Encapsulate complex logic in service classes or functions located in `backend/services/`.
- Route handlers should call these services and return structured responses.
- This separation mirrors the frontend approach of organizing reusable components.

## 4. Database and Async Operations
- Use SQLAlchemy models from `backend/database/models.py` with async sessions.
- Provide a dependency (`get_db`) to inject `AsyncSession` into routes.
- Keep database transactions short and avoid blocking calls so the API remains responsive.

## 5. Caching and Redis
- Introduce a small caching utility that wraps Redis operations.
- Cache organization and learning responses keyed by user and request payload when appropriate.
- Allow the frontend to request fresh data with `/api/v1/chat/fresh` or by including a `force_refresh` flag.

## 6. Error Handling
- Return errors using the shared `ErrorResponse` model.
- Log exceptions with meaningful messages but avoid leaking internal details to the client.
- Align HTTP status codes with frontend expectations for easier error handling in React components.

## 7. Testing Patterns
- Provide pytest fixtures for database setup and crew overrides (see `adhd-focus-hub/tests`).
- Write unit tests for each service function and route to ensure data contracts remain stable.

## 8. Future Enhancements
- Abstract a common `AIInteractionService` for features that call CrewAI agents.
- Persist conversation history in Redis so subsequent requests can reuse prior context.
- Document any schema changes in `ROADMAP.md` to keep frontend and backend aligned.

---
These patterns complement the frontend component guidelines and help maintain a clear contract between the two layers. Work closely with the FrontendArchitect to keep API paths and data models synchronized.
