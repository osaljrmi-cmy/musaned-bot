import os
import sys
from rq import Worker, Queue
from redis import Redis


# نفس اسم الـ queue الذي تستخدمه في enqueue
LISTEN = ["musaned"]


def main() -> None:
    redis_url = os.getenv("REDIS_URL")  # Render env var
    if not redis_url:
        raise RuntimeError("REDIS_URL is not set")

    conn = Redis.from_url(redis_url)

    # Logs واضحة في Render
    print(f"[worker] starting; queues={LISTEN}", flush=True)
    print(f"[worker] redis_url set: {'yes' if redis_url else 'no'}", flush=True)

    queues = [Queue(name, connection=conn, default_result_ttl=3600) for name in LISTEN]
    worker = Worker(queues, connection=conn)

    # لا نحتاج scheduler حالياً
    worker.work(with_scheduler=False)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[worker] fatal error: {e}", file=sys.stderr, flush=True)
        raise