# Conversation History Persistence and Caching Design

This document outlines how conversation history will be stored in Postgres and cached in Redis.

## Goals
- Persist all user conversations for long‑term retrieval.
- Cache recent history in Redis for fast access and context sharing.
- Keep the caching layer simple and automatically purged.

## Database Schema
We will create a `conversation_history` table with the following fields:
- `id` &ndash; primary key.
- `user_id` &ndash; foreign key to `users.id` (nullable until auth fully integrated).
- `message` &ndash; text of the user request.
- `response` &ndash; text returned by the crew.
- `metadata` &ndash; JSON blob for agent and routing details.
- `created_at` &ndash; timestamp of the interaction.

## Alembic Migration
A new migration `0002_conversation_history.py` will:
1. Create the `conversation_history` table with the columns above.
2. Provide a downgrade step to drop the table.
3. Use the same numbering scheme as existing migrations.

Developers run `alembic upgrade head` after pulling the change to create the table.

## Redis Caching Strategy
- Store a Redis list per user: key format `conversation:{user_id}`.
- Each list item is a JSON record mirroring a row of `conversation_history`.
- Push new interactions with `LPUSH` and trim with `LTRIM` to a configured limit (e.g., last 50 messages).
- Set a TTL (e.g., 24 hours) on each key so inactive histories expire automatically.
- When fetching history for a request, read from Redis first; if missing, load the most recent records from Postgres and populate the cache.

## Implementation Notes
- Use `redis.asyncio` to interact with Redis from FastAPI.
- The caching helper can live in `backend/services/cache.py`.
- Conversation saving occurs in a background task to avoid blocking API responses.
- Future work may include indexing on `user_id` and pagination endpoints.
