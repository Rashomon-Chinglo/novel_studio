from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column

from app.core import new_id, utc_now
from app.persistence.db.base import Base


class ChapterSummary(AsyncAttrs, Base):
    __tablename__ = "chapter_summaries"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id, index=True)
    bible_id: Mapped[str] = mapped_column(
        String, ForeignKey("bibles.id"), nullable=False, index=True
    )
    substory_id: Mapped[str] = mapped_column(
        String, ForeignKey("substories.id"), nullable=False, index=True
    )
    chapter_index: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    written_chapter_id: Mapped[str] = mapped_column(
        String, ForeignKey("written_chapters.id"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(String, nullable=False)
    workflow_run_id: Mapped[str] = mapped_column(
        String, ForeignKey("workflow_runs.id"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False, index=True
    )


class CumulativeSubstorySummary(AsyncAttrs, Base):
    __tablename__ = "cumulative_substory_summaries"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id, index=True)
    bible_id: Mapped[str] = mapped_column(
        String, ForeignKey("bibles.id"), nullable=False, index=True
    )
    substory_id: Mapped[str] = mapped_column(
        String, ForeignKey("substories.id"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(String, nullable=False)
    workflow_run_id: Mapped[str] = mapped_column(
        String, ForeignKey("workflow_runs.id"), nullable=False, index=True
    )
    chapter_index: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    written_chapter_id: Mapped[str] = mapped_column(
        String, ForeignKey("written_chapters.id"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False, index=True
    )
