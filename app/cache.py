from __future__ import annotations
import json
from typing import Any, Optional, Callable
import redis
from .database import get_settings

_redis_client: Optional[redis.Redis] = None

def get_redis() -> redis.Redis:
    global _redis_client
    if _redis_client is None:
        s = get_settings()
        _redis_client = redis.Redis(host=s.REDIS_HOST, port=s.REDIS_PORT, db=s.REDIS_DB, decode_responses=True)
    return _redis_client

def cache_set(key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
    r = get_redis()
    data = json.dumps(value)
    if ttl_seconds is None:
        ttl_seconds = get_settings().REDIS_CACHE_TTL_SECONDS
    r.setex(key, ttl_seconds, data)

def cache_get(key: str) -> Optional[Any]:
    r = get_redis()
    data = r.get(key)
    if data is None:
        return None
    return json.loads(data)

def cache_del(pattern: str) -> None:
    r = get_redis()
    for k in r.scan_iter(pattern):
        r.delete(k)
