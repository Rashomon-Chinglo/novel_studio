from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.persistence.db.session import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class WorkflowRun(AsyncAttrs, Base):
    __tablename__ = "workflow_runs"
    id = Column(String, primary_key=True, index=True)
    workflow_type = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, index=True)
    current_stage = Column(String, index=True)
    bible_id = Column(String, ForeignKey("bibles.id"), nullable=False, index=True)
    substory_id = Column(String, ForeignKey("substories.id"), nullable=False, index=True)
    chapter_index = Column(Integer, nullable=False, index=True)
    error_code = Column(String, index=True)
    error_message = Column(String, index=True)
    started_at = Column(DateTime, default=utc_now, nullable=False, index=True)
    finished_at = Column(DateTime, nullable=True, index=True)
