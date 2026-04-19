from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column

from app.core import new_id, utc_now
from app.persistence.db.base import Base


class Bible(AsyncAttrs, Base):
    __tablename__ = "bibles"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id, index=True)
    content: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False, index=True
    )


class Substory(AsyncAttrs, Base):
    __tablename__ = "substories"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id, index=True)
    bible_id: Mapped[str] = mapped_column(
        String, ForeignKey("bibles.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    content: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False, index=True
    )


class ChapterBlueprint(AsyncAttrs, Base):
    __tablename__ = "chapter_blueprints"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id, index=True)
    chapter_index: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    substory_id: Mapped[str] = mapped_column(
        String, ForeignKey("substories.id"), nullable=False, index=True
    )
    bible_id: Mapped[str] = mapped_column(
        String, ForeignKey("bibles.id"), nullable=False, index=True
    )
    content: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    workflow_run_id: Mapped[str] = mapped_column(
        String, ForeignKey("workflow_runs.id"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False, index=True
    )


class ChapterOutline(AsyncAttrs, Base):
    __tablename__ = "chapter_outlines"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id, index=True)
    bible_id: Mapped[str] = mapped_column(
        String, ForeignKey("bibles.id"), nullable=False, index=True
    )
    chapter_blueprint_id: Mapped[str] = mapped_column(
        String, ForeignKey("chapter_blueprints.id"), nullable=False, index=True
    )
    substory_id: Mapped[str] = mapped_column(
        String, ForeignKey("substories.id"), nullable=False, index=True
    )
    chapter_index: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    content: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    workflow_run_id: Mapped[str] = mapped_column(
        String, ForeignKey("workflow_runs.id"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False, index=True
    )
