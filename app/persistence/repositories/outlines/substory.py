from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models.outline import Substory


class SubstoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, substory_id: str) -> Substory | None:
        return await self.session.get(Substory, substory_id)

    def add(self, substory: Substory) -> None:
        self.session.add(substory)

    async def list_by_bible(self, bible_id: str) -> Sequence[Substory]:
        result = await self.session.execute(
            select(Substory)
            .where(Substory.bible_id == bible_id)
            .order_by(Substory.order_index.asc(), Substory.created_at.asc())
        )
        return result.scalars().all()
