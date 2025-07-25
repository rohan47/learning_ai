from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from redis.asyncio import Redis

from config.settings import get_settings

settings = get_settings()

redis_client = Redis.from_url(settings.redis_url, decode_responses=True)

CACHE_LIMIT = int(os.getenv("CONVERSATION_CACHE_LIMIT", "50"))
CACHE_TTL = int(os.getenv("CONVERSATION_CACHE_TTL", str(60 * 60 * 24)))


def _key(user_id: Optional[int]) -> str:
    return f"conversation:{user_id or 'anon'}"


async def push_history(user_id: Optional[int], record: Dict[str, Any]) -> None:
    key = _key(user_id)
    await redis_client.lpush(key, json.dumps(record))
    await redis_client.ltrim(key, 0, CACHE_LIMIT - 1)
    await redis_client.expire(key, CACHE_TTL)


async def get_history(
    user_id: Optional[int], limit: int = CACHE_LIMIT
) -> List[Dict[str, Any]]:
    key = _key(user_id)
    data = await redis_client.lrange(key, 0, limit - 1)
    return [json.loads(d) for d in data]
