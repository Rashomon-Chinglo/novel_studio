from datetime import UTC, datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.persistence.db.base import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class Bible(AsyncAttrs, Base):
    __tablename__ = "bibles"
    id = Column(String, primary_key=True, index=True)
    content = Column(JSON, nullable=False)
    workflow_run_id = Column(String, ForeignKey("workflow_runs.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)


class Substory(AsyncAttrs, Base):
    __tablename__ = "substories"
    id = Column(String, primary_key=True, index=True)
    bible_id = Column(String, ForeignKey("bibles.id"), nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    order_index = Column(Integer, nullable=False, index=True)
    content = Column(JSON, nullable=False)
    workflow_run_id = Column(String, ForeignKey("workflow_runs.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)


class ChapterBlueprint(AsyncAttrs, Base):
    __tablename__ = "chapter_blueprints"
    id = Column(String, primary_key=True, index=True)
    chapter_index = Column(Integer, nullable=False, index=True)
    substory_id = Column(String, ForeignKey("substories.id"), nullable=False, index=True)
    bible_id = Column(String, ForeignKey("bibles.id"), nullable=False, index=True)
    content = Column(JSON, nullable=False)
    workflow_run_id = Column(String, ForeignKey("workflow_runs.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)


class ChapterOutline(AsyncAttrs, Base):
    __tablename__ = "chapter_outlines"
    id = Column(String, primary_key=True, index=True)
    bible_id = Column(String, ForeignKey("bibles.id"), nullable=False, index=True)
    chapter_blueprint_id = Column(
        String, ForeignKey("chapter_blueprints.id"), nullable=False, index=True
    )
    substory_id = Column(String, ForeignKey("substories.id"), nullable=False, index=True)
    chapter_index = Column(Integer, nullable=False, index=True)
    content = Column(JSON, nullable=False)
    workflow_run_id = Column(String, ForeignKey("workflow_runs.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)
