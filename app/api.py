from datetime import tzinfo, timezone
from zoneinfo import ZoneInfo
import json
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.schemas import EventIn, EventOut
from app.models import Event
from app.settings import get_settings

settings = get_settings()
router = APIRouter()

LOCAL_TZ = ZoneInfo("Asia/Shanghai")


def verify_token(x_api_token: str | None = Header(default=None)):
    if settings.API_TOKEN is None:
        return
    if x_api_token != settings.API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")


def to_local(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(LOCAL_TZ)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/events", response_model=EventOut, dependencies=[Depends(verify_token)])
def create_event(event: EventIn, db: Session = Depends(get_db)):
    obj = Event(type=event.type, payload=json.dumps(event.payload))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {
        "id": obj.id,
        "type": obj.type,
        "payload": event.payload,
        "created_at": to_local(obj.created_at),
    }


@router.get("/events", response_model=list[EventOut], dependencies=[Depends(verify_token)])
def list_events(db: Session = Depends(get_db)):
    items = db.query(Event).order_by(Event.id.desc()).all()
    return [
        {
            "id": e.id,
            "type": e.type,
            "payload": json.loads(e.payload),
            "created_at": to_local(e.created_at),
        }
        for e in items
    ]
