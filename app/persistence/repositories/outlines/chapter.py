from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models.outline import ChapterOutline


class ChapterOutlineRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, chapter_id: str) -> ChapterOutline | None:
        return await self.session.get(ChapterOutline, chapter_id)

    def add(self, chapter: ChapterOutline) -> None:
        self.session.add(chapter)

    async def list_by_substory(self, substory_id: str) -> Sequence[ChapterOutline]:
        result = await self.session.execute(
            select(ChapterOutline)
            .where(ChapterOutline.substory_id == substory_id)
            .order_by(ChapterOutline.order_index.asc(), ChapterOutline.created_at.asc())
        )
        return result.scalars().all()
