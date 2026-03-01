import traceback
from app.flows.state_machine import handle_event


def process_event(
    wa_id: str,
    text: str | None,
    image_media_id: str | None
) -> None:
    try:
        print(f"[task] processing event for wa_id={wa_id}", flush=True)

        handle_event(
            wa_id=wa_id,
            text=text,
            image_media_id=image_media_id,
        )

        print(f"[task] done for wa_id={wa_id}", flush=True)

    except Exception as e:
        print(f"[task] error for wa_id={wa_id}: {e}", flush=True)
        traceback.print_exc()
        raise