import json
import os
import time
from redis import Redis
from app.sessions.models import Session


def _session_key(wa_id: str) -> str:
    return f"session:{wa_id}"


def _lock_key(wa_id: str) -> str:
    return f"lock:{wa_id}"


def get_redis() -> Redis:
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        raise RuntimeError("REDIS_URL is not set")
    return Redis.from_url(redis_url, decode_responses=True)


def get_session(wa_id: str) -> Session:
    r = get_redis()
    raw = r.get(_session_key(wa_id))
    if raw:
        return Session.model_validate(json.loads(raw))
    return Session(wa_id=wa_id, updated_at=time.time())


def save_session(session: Session) -> None:
    r = get_redis()
    session.updated_at = time.time()
    r.set(_session_key(session.wa_id), session.model_dump_json())
    r.expire(_session_key(session.wa_id), 15 * 60)


def reset_session(wa_id: str) -> Session:
    session = Session(wa_id=wa_id, state="IDLE", updated_at=time.time())
    save_session(session)
    return session


def acquire_lock(wa_id: str, ttl_seconds: int = 15 * 60) -> bool:
    r = get_redis()
    return bool(r.set(_lock_key(wa_id), "1", nx=True, ex=ttl_seconds))


def release_lock(wa_id: str) -> None:
    r = get_redis()
    r.delete(_lock_key(wa_id))