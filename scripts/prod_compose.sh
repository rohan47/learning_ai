#!/usr/bin/env bash
# Build and run the production stack using Docker Compose.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

docker compose -f docker-compose.production.yml up --build -d
