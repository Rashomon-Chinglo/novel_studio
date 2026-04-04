from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.core import new_id, utc_now
from app.persistence.db.base import Base


class ChapterSummary(AsyncAttrs, Base):
    __tablename__ = "chapter_summaries"
    id = Column(String, primary_key=True, default=new_id, index=True)
    bible_id = Column(String, ForeignKey("bibles.id"), nullable=False, index=True)
    substory_id = Column(String, ForeignKey("substories.id"), nullable=False, index=True)
    chapter_index = Column(Integer, nullable=False, index=True)
    written_chapter_id = Column(
        String, ForeignKey("written_chapters.id"), nullable=False, index=True
    )
    content = Column(String, nullable=False)
    workflow_run_id = Column(String, ForeignKey("workflow_runs.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)


class CumulativeSubstorySummary(AsyncAttrs, Base):
    __tablename__ = "cumulative_substory_summaries"
    id = Column(String, primary_key=True, default=new_id, index=True)
    bible_id = Column(String, ForeignKey("bibles.id"), nullable=False, index=True)
    substory_id = Column(String, ForeignKey("substories.id"), nullable=False, index=True)
    content = Column(String, nullable=False)
    workflow_run_id = Column(String, ForeignKey("workflow_runs.id"), nullable=False, index=True)
    chapter_index = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)
