from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column

from app.core import new_id, utc_now
from app.persistence.db.base import Base


class Snippet(AsyncAttrs, Base):
    __tablename__ = "snippets"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id, index=True)
    title: Mapped[str | None] = mapped_column(String, index=True)
    category: Mapped[str | None] = mapped_column(String, index=True)
    tags: Mapped[str | None] = mapped_column(String, index=True)
    mood: Mapped[str | None] = mapped_column(String, index=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=utc_now, index=True)
    content: Mapped[str | None] = mapped_column(Text)
