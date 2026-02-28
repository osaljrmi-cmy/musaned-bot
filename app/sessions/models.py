from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class Session(BaseModel):
    wa_id: str
    state: str = "IDLE"
    selected_operation: Optional[int] = None
    last_image_media_id: Optional[str] = None
    last_text: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    lock: bool = False
    updated_at: float = 0.0
