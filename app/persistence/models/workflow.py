from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column

from app.core import new_id, utc_now
from app.domain.workflow import WorkflowErrorCode, WorkflowStage, WorkflowStatus, WorkflowType
from app.persistence.db.base import Base


class WorkflowRun(AsyncAttrs, Base):
    __tablename__ = "workflow_runs"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id, index=True)
    workflow_type: Mapped[WorkflowType] = mapped_column(String, nullable=False, index=True)
    status: Mapped[WorkflowStatus] = mapped_column(String, nullable=False, index=True)
    current_stage: Mapped[WorkflowStage] = mapped_column(String, nullable=False, index=True)
    bible_id: Mapped[str] = mapped_column(
        String, ForeignKey("bibles.id"), nullable=False, index=True
    )
    substory_id: Mapped[str] = mapped_column(
        String, ForeignKey("substories.id"), nullable=False, index=True
    )
    chapter_outline_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("chapter_outlines.id"), nullable=True, index=True
    )
    chapter_index: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    error_code: Mapped[WorkflowErrorCode | None] = mapped_column(String, nullable=True, index=True)
    error_message: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False, index=True
    )
    substory_chapter_index: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)
