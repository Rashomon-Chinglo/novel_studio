from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.core import new_id, utc_now
from app.persistence.db.base import Base


class WrittenChapter(AsyncAttrs, Base):
    __tablename__ = "written_chapters"
    id = Column(String, primary_key=True, default=new_id, index=True)
    bible_id = Column(String, ForeignKey("bibles.id"), nullable=False, index=True)
    substory_id = Column(String, ForeignKey("substories.id"), nullable=False, index=True)
    chapter_outline_id = Column(
        String, ForeignKey("chapter_outlines.id"), nullable=False, index=True
    )
    workflow_run_id = Column(String, ForeignKey("workflow_runs.id"), nullable=False, index=True)
    chapter_index = Column(Integer, nullable=False, index=True)
    content = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)
