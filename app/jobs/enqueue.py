from rq import Queue
import redis
from app.settings import settings

redis_conn = redis.Redis.from_url(settings.REDIS_URL)
q = Queue(""musaned"", connection=redis_conn)

def enqueue_process_event(wa_id: str, text: str | None, image_media_id: str | None) -> None:
    q.enqueue(""app.jobs.tasks.process_event"", wa_id, text, image_media_id, job_timeout=600)
