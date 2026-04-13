from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column

from app.core import new_id, utc_now
from app.persistence.db.base import Base


class Snippet(AsyncAttrs, Base):
    __tablename__ = "snippets"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, nullable=False, default=new_id, index=True
    )
    # title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    category: Mapped[str] = mapped_column(String, index=True, nullable=False)
    tags: Mapped[str] = mapped_column(String, index=True, nullable=False)
    mood: Mapped[str] = mapped_column(String, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
