# Docker-Based Deployment Architecture

This document describes how the backend and frontend services are deployed using Docker.

## Overview

We use **Docker Compose** to orchestrate four main services:

1. **backend** – FastAPI application built from `backend/Dockerfile`.
2. **frontend** – React application built from `frontend/Dockerfile`.
3. **postgres** – PostgreSQL database for persistent storage.
4. **redis** – Redis cache used for conversation history.

Two compose files are provided:

- `docker-compose.yml` – optimized for local development with volume mounts and automatic reload.
- `docker-compose.production.yml` – builds versioned images for production deployments.

## Local Development

Run:

```bash
docker compose up --build
```

The development compose file mounts the source code so changes are immediately reflected. The backend runs with `uvicorn --reload` and the frontend with `npm start`.

## Production Deployment

The production compose file builds minimal images and starts containers without volume mounts. Environment variables control secrets and connection URLs. Example:

```bash
docker compose -f docker-compose.production.yml up --build -d
```

Images can be pushed to a container registry and reused across environments.

## Networking

All services share an internal network created by Docker Compose. The frontend communicates with the backend on port `8000`, while the backend talks to PostgreSQL and Redis on their default ports. Ports `3000`, `8000`, `5432`, and `6379` are published for external access.

## Persistence

Database and cache data are stored in Docker volumes (`postgres_data`, `redis_data`). These volumes survive container restarts to preserve user data and cached history.

---

This architecture provides a repeatable way to run the application locally and in production while isolating dependencies and simplifying deployment steps.
