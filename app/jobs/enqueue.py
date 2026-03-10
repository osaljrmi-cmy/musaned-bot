import os
from rq import Queue
from redis import Redis
from app.jobs.tasks import process_event


QUEUE_NAME = "musaned"


def get_queue() -> Queue:
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        raise RuntimeError("REDIS_URL is not set")

    conn = Redis.from_url(redis_url)
    return Queue(QUEUE_NAME, connection=conn)


def enqueue_process_event(
    wa_id: str,
    text: str | None,
    image_media_id: str | None
) -> None:
    queue = get_queue()

    queue.enqueue(
        process_event,
        wa_id=wa_id,
        text=text,
        image_media_id=image_media_id,
        job_timeout=600,
    )