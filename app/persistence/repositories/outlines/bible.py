from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models.outline import Bible


class BibleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, bible_id: str) -> Bible | None:
        return await self.session.get(Bible, bible_id)

    def add(self, bible: Bible) -> None:
        self.session.add(bible)

    async def list_all(self) -> Sequence[Bible]:
        result = await self.session.execute(select(Bible).order_by(Bible.created_at.desc()))
        return result.scalars().all()
