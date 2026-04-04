from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.core import new_id, utc_now
from app.persistence.db.base import Base


class WorkflowRun(AsyncAttrs, Base):
    __tablename__ = "workflow_runs"
    id = Column(String, primary_key=True, default=new_id, index=True)
    workflow_type = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, index=True)
    current_stage = Column(String, nullable=False, index=True)
    bible_id = Column(String, ForeignKey("bibles.id"), nullable=True, index=True)
    substory_id = Column(String, ForeignKey("substories.id"), nullable=True, index=True)
    chapter_outline_id = Column(
        String, ForeignKey("chapter_outlines.id"), nullable=True, index=True
    )
    chapter_index = Column(Integer, nullable=True, index=True)
    error_code = Column(String, nullable=True, index=True)
    error_message = Column(String, nullable=True, index=True)
    started_at = Column(DateTime, default=utc_now, nullable=False, index=True)
    finished_at = Column(DateTime, nullable=True, index=True)
