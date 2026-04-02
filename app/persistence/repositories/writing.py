from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models.writing import WrittenChapter


class WrittenChapterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, chapter_id: str) -> WrittenChapter | None:
        return await self.session.get(WrittenChapter, chapter_id)

    def add(self, chapter: WrittenChapter) -> None:
        self.session.add(chapter)

    async def list_by_substory(self, substory_id: str) -> Sequence[WrittenChapter]:
        result = await self.session.execute(
            select(WrittenChapter)
            .where(WrittenChapter.substory_id == substory_id)
            .order_by(WrittenChapter.chapter_index.asc())
        )
        return result.scalars().all()

    async def list_by_chapter_outline(self, chapter_outline_id: str) -> Sequence[WrittenChapter]:
        result = await self.session.execute(
            select(WrittenChapter)
            .where(WrittenChapter.chapter_outline_id == chapter_outline_id)
            .order_by(WrittenChapter.created_at.desc())
        )
        return result.scalars().all()

    async def get_latest_chapter(self, bible_id: str) -> WrittenChapter | None:
        result = await self.session.execute(
            select(WrittenChapter)
            .where(WrittenChapter.bible_id == bible_id)
            .order_by(WrittenChapter.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_latest_chapter_by_substory(self, substory_id: str) -> WrittenChapter | None:
        result = await self.session.execute(
            select(WrittenChapter)
            .where(WrittenChapter.substory_id == substory_id)
            .order_by(WrittenChapter.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
