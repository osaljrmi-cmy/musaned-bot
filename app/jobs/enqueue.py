import os
from rq import Queue
from redis import Redis


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
        "app.jobs.tasks.process_event",
        wa_id,
        text,
        image_media_id,
        job_timeout=600
    )