from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.db.session import Base


class Snippet(AsyncAttrs, Base):
    __tablename__ = "snippets"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String, index=True)
    tags = Column(String, index=True)
    mood = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    content = Column(Text)
