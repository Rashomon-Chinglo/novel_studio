from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models.outline import Chapter


class ChapterRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, chapter_id: str) -> Chapter | None:
        return await self.session.get(Chapter, chapter_id)

    def add(self, chapter: Chapter) -> None:
        self.session.add(chapter)

    async def list_by_substory(self, substory_id: str) -> Sequence[Chapter]:
        result = await self.session.execute(
            select(Chapter)
            .where(Chapter.substory_id == substory_id)
            .order_by(Chapter.order_index.asc(), Chapter.created_at.asc())
        )
        return result.scalars().all()
