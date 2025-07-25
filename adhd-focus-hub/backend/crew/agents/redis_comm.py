import redis
import json
from backend.config.settings import get_settings

settings = get_settings()

class RedisAgentComm:
    def __init__(self):
        self.client = redis.Redis.from_url(settings.redis_url)

    def publish(self, channel: str, message: dict):
        self.client.publish(channel, json.dumps(message))

    def subscribe(self, channel: str):
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel)
        return pubsub
