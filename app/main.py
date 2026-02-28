from fastapi import FastAPI, Request, HTTPException
from app.settings import settings
from app.whatsapp.webhook_parser import parse_webhook
from app.jobs.enqueue import enqueue_process_event

app = FastAPI()


# -------------------------
# Health Check
# -------------------------
@app.get("/health")
def health():
    return {"ok": True}


# -------------------------
# Webhook Verification (Meta)
# -------------------------
@app.get("/webhook")
def verify_webhook(request: Request):
    params = dict(request.query_params)

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == settings.VERIFY_TOKEN:
        return int(challenge)

    raise HTTPException(status_code=403, detail="Verification failed")


# -------------------------
# Webhook Receiver
# -------------------------
@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()

    wa_id, text, image_media_id = parse_webhook(payload)

    # إذا لا يوجد رسالة صالحة
    if not wa_id:
        return {"ok": True}

    enqueue_process_event(
        wa_id=wa_id,
        text=text,
        image_media_id=image_media_id
    )

    return {"ok": True}