import json
import time
import redis
from app.settings import settings
from app.sessions.models import Session

r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def _session_key(wa_id: str) -> str:
    return f""session:{wa_id}""

def get_session(wa_id: str) -> Session:
    raw = r.get(_session_key(wa_id))
    if raw:
        return Session.model_validate(json.loads(raw))
    return Session(wa_id=wa_id, updated_at=time.time())

def save_session(session: Session) -> None:
    session.updated_at = time.time()
    r.set(_session_key(session.wa_id), session.model_dump_json())
    r.expire(_session_key(session.wa_id), 15 * 60)

def reset_session(wa_id: str) -> Session:
    session = Session(wa_id=wa_id, state=""IDLE"", updated_at=time.time())
    save_session(session)
    return session

def acquire_lock(wa_id: str, ttl_seconds: int = 15 * 60) -> bool:
    key = f""lock:{wa_id}""
    return bool(r.set(key, ""1"", nx=True, ex=ttl_seconds))

def release_lock(wa_id: str) -> None:
    r.delete(f""lock:{wa_id}"")
