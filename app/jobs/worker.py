import os
from redis import Redis
from rq import Worker, Queue

# نفس اسم الـ queue المستخدم في enqueue
LISTEN = ["musaned"]

def main() -> None:
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        raise RuntimeError("REDIS_URL is not set")

    conn = Redis.from_url(redis_url)

    queues = [Queue(name, connection=conn) for name in LISTEN]
    worker = Worker(queues, connection=conn)
    worker.work(with_scheduler=False)

if __name__ == "__main__":
    main()