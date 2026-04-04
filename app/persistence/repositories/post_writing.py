from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models.post_writing import ChapterSummary, CumulativeSubstorySummary


class ChapterSummaryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, chapter_summary_id: str) -> ChapterSummary | None:
        return await self.session.get(ChapterSummary, chapter_summary_id)

    async def get_by_written_chapter(self, written_chapter_id: str) -> ChapterSummary | None:
        result = await self.session.execute(
            select(ChapterSummary)
            .where(ChapterSummary.written_chapter_id == written_chapter_id)
            .limit(1)
        )
        return result.scalar_one_or_none()

    def add(self, chapter: ChapterSummary) -> None:
        self.session.add(chapter)

    async def list_by_substory(self, substory_id: str) -> Sequence[ChapterSummary]:
        result = await self.session.execute(
            select(ChapterSummary)
            .where(ChapterSummary.substory_id == substory_id)
            .order_by(ChapterSummary.chapter_index.asc())
        )
        return result.scalars().all()

    async def get_latest_by_bible(self, bible_id: str) -> ChapterSummary | None:
        result = await self.session.execute(
            select(ChapterSummary)
            .where(ChapterSummary.bible_id == bible_id)
            .order_by(ChapterSummary.chapter_index.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()


class CumulativeSubstorySummaryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, cumulative_substory_summary_id: str) -> CumulativeSubstorySummary | None:
        return await self.session.get(CumulativeSubstorySummary, cumulative_substory_summary_id)

    def add(self, substory: CumulativeSubstorySummary) -> None:
        self.session.add(substory)

    async def list_by_substory(self, substory_id: str) -> Sequence[CumulativeSubstorySummary]:
        result = await self.session.execute(
            select(CumulativeSubstorySummary)
            .where(CumulativeSubstorySummary.substory_id == substory_id)
            .order_by(CumulativeSubstorySummary.chapter_index.asc())
        )
        return result.scalars().all()

    async def get_latest_by_bible(self, bible_id: str) -> CumulativeSubstorySummary | None:
        result = await self.session.execute(
            select(CumulativeSubstorySummary)
            .where(CumulativeSubstorySummary.bible_id == bible_id)
            .order_by(CumulativeSubstorySummary.chapter_index.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_latest_by_substory(self, substory_id: str) -> CumulativeSubstorySummary | None:
        result = await self.session.execute(
            select(CumulativeSubstorySummary)
            .where(CumulativeSubstorySummary.substory_id == substory_id)
            .order_by(CumulativeSubstorySummary.chapter_index.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
