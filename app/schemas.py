from datetime import datetime
from pydantic import BaseModel


class EventIn(BaseModel):
    type: str
    payload: dict

class EventOut(BaseModel):
    id: int
    type: str
    payload: dict
    created_at: datetime