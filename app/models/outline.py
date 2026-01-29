from datetime import UTC, datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.db.session import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class Bible(AsyncAttrs, Base):
    __tablename__ = "bibles"
    id = Column(String, primary_key=True, index=True)
    content = Column(JSON)
    created_at = Column(DateTime, default=utc_now, index=True)


class Substory(AsyncAttrs, Base):
    __tablename__ = "substories"
    id = Column(String, primary_key=True, index=True)
    bible_id = Column(String, ForeignKey("bibles.id"), index=True)
    title = Column(String, index=True)
    order_index = Column(Integer, index=True)
    content = Column(JSON)
    created_at = Column(DateTime, default=utc_now, index=True)


class Chapter(AsyncAttrs, Base):
    __tablename__ = "chapters"
    id = Column(String, primary_key=True, index=True)
    substory_id = Column(String, ForeignKey("substories.id"), index=True)
    title = Column(String, index=True)
    order_index = Column(Integer, index=True)
    content = Column(JSON)
    created_at = Column(DateTime, default=utc_now, index=True)
