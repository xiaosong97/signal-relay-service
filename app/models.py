from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, timezone
from app.db import Base

# 业务数据模型（ORM → 表结构）


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    type = Column(String(64), nullable=False)
    payload = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
