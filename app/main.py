from fastapi import FastAPI, Request, HTTPException
from app.settings import settings
from app.whatsapp.webhook_parser import parse_webhook
from app.jobs.enqueue import enqueue_process_event

app = FastAPI()


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/webhook")
def verify_webhook(request: Request):
    params = dict(request.query_params)

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == settings.VERIFY_TOKEN:
        return int(challenge)

    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def webhook(request: Request):
    try:
        payload = await request.json()
    except Exception:
        # لا نكسر الـ webhook حتى لو جاء body غير JSON
        return {"ok": True}

    wa_id, text, image_media_id = parse_webhook(payload)

    # status updates أو events بدون messages
    if not wa_id:
        return {"ok": True}

    print(f"[webhook] received event wa_id={wa_id} type={'image' if image_media_id else 'text'}", flush=True)

    enqueue_process_event(
        wa_id=wa_id,
        text=text,
        image_media_id=image_media_id,
    )

    return {"ok": True}


# (اختياري) Endpoint داخلي للاختبار بدون Meta
@app.post("/debug/enqueue")
async def debug_enqueue(request: Request):
    body = await request.json()
    wa_id = body.get("wa_id", "967700000000")
    text = body.get("text")
    image_media_id = body.get("image_media_id")

    enqueue_process_event(wa_id=wa_id, text=text, image_media_id=image_media_id)
    return {"ok": True, "enqueued_for": wa_id}