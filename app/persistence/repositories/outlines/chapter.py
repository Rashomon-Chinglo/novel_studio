from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models.outline import ChapterBlueprint, ChapterOutline


class ChapterOutlineRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, outline_id: str) -> ChapterOutline | None:
        return await self.session.get(ChapterOutline, outline_id)

    def add(self, outline: ChapterOutline) -> None:
        self.session.add(outline)

    async def get_latest(self, bible_id: str) -> ChapterOutline | None:
        result = await self.session.execute(
            select(ChapterOutline)
            .where(ChapterOutline.bible_id == bible_id)
            .order_by(ChapterOutline.chapter_index.desc())
            .limit(1)
        )
        return result.scalars().first()

    async def list_by_substory(self, substory_id: str) -> Sequence[ChapterOutline]:
        result = await self.session.execute(
            select(ChapterOutline)
            .where(ChapterOutline.substory_id == substory_id)
            .order_by(ChapterOutline.chapter_index.asc(), ChapterOutline.created_at.asc())
        )
        return result.scalars().all()


class ChapterBlueprintRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, blueprint_id: str) -> ChapterBlueprint | None:
        return await self.session.get(ChapterBlueprint, blueprint_id)

    def add(self, blueprint: ChapterBlueprint) -> None:
        self.session.add(blueprint)

    async def list_by_substory(self, substory_id: str) -> Sequence[ChapterBlueprint]:
        result = await self.session.execute(
            select(ChapterBlueprint)
            .where(ChapterBlueprint.substory_id == substory_id)
            .order_by(ChapterBlueprint.chapter_index.asc(), ChapterBlueprint.created_at.asc())
        )
        return result.scalars().all()

    async def get_latest(self, bible_id: str) -> ChapterBlueprint | None:
        result = await self.session.execute(
            select(ChapterBlueprint)
            .where(ChapterBlueprint.bible_id == bible_id)
            .order_by(ChapterBlueprint.chapter_index.desc())
            .limit(1)
        )
        return result.scalars().first()
