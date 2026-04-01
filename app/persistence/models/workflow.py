from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.persistence.db.session import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class WorkflowRun(AsyncAttrs, Base):
    __tablename__ = "workflow_runs"
    id = Column(String, primary_key=True, index=True)
    workflow_type = Column(String, index=True)
    status = Column(String, index=True)
    current_stage = Column(String, index=True)
    bible_id = Column(String, ForeignKey("bibles.id"), index=True)
    substory_id = Column(String, ForeignKey("substories.id"), index=True)
    chapter_index = Column(Integer, index=True)
    error_code = Column(String, index=True)
    error_message = Column(String, index=True)
    started_at = Column(DateTime, default=utc_now, index=True)
    finished_at = Column(DateTime, default=utc_now, index=True)
