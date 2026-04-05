from collections.abc import Callable

from app.modules.base import ChapterSummary as ChapterSummarySchema
from app.modules.base import CumulativeSubstorySummary as CumulativeSubstorySummarySchema
from app.modules.outlines.schemas import Bible as BibleSchema
from app.modules.outlines.schemas import ChapterBlueprint as ChapterBlueprintSchema
from app.modules.outlines.schemas import (
    ChapterOriginalSubstoryNodes as ChapterOriginalSubstoryNodesSchema,
)
from app.modules.outlines.schemas import ChapterOutline as ChapterOutlineSchema
from app.modules.outlines.schemas import Substory as SubstorySchema
from app.modules.writing import MaterialProvider, WritingEngine
from app.modules.writing import SceneChunk as SceneChunkSchema
from app.modules.writing import WrittenChapter as WrittenChapterSchema
from app.persistence import SqlAlchemyUnitOfWork
from app.persistence.models import WrittenChapter


class WritingService:
    def __init__(
        self,
        uow_factory: Callable[[], SqlAlchemyUnitOfWork] = SqlAlchemyUnitOfWork,
        engine_factory: Callable[[MaterialProvider], WritingEngine] = WritingEngine,
        material_provider_factory: Callable[[], MaterialProvider] = MaterialProvider,
    ) -> None:
        self.uow_factory: Callable[[], SqlAlchemyUnitOfWork] = uow_factory
        self.engine: WritingEngine = engine_factory(material_provider_factory())

    def _to_schema(self, written_chapter: WrittenChapter) -> WrittenChapterSchema:
        return WrittenChapterSchema(**written_chapter.content)

    async def create(
        self,
        *,
        written_chapter: WrittenChapterSchema,
        chapter_outline_id: str,
    ) -> str:
        async with self.uow_factory() as uow:
            chapter_outline = await uow.outlines.chapter_outlines.get(chapter_outline_id)
            if chapter_outline is None:
                raise ValueError(f"Chapter outline with id {chapter_outline_id} not found.")

            writing = WrittenChapter(
                bible_id=chapter_outline.bible_id,
                substory_id=chapter_outline.substory_id,
                chapter_outline_id=chapter_outline_id,
                workflow_run_id=chapter_outline.workflow_run_id,
                chapter_index=chapter_outline.chapter_index,
                content=written_chapter.model_dump(),
            )
            uow.writing.written_chapters.add(writing)
            await uow.commit()
            return writing.id

    async def generate(
        self,
        *,
        bible: BibleSchema,
        substory: SubstorySchema,
        original_logic_nodes: ChapterOriginalSubstoryNodesSchema,
        chapter_blueprint: ChapterBlueprintSchema,
        chapter_outline: ChapterOutlineSchema,
        pre_chapter_summary: ChapterSummarySchema,
        cumulative_substory_summary: CumulativeSubstorySummarySchema,
        previous_scene_chunk: SceneChunkSchema | None = None,
    ) -> WrittenChapterSchema:
        written_chapter = await self.engine.writing(
            self.engine.ChapterWritingContext(
                bible=bible,
                substory=substory,
                original_logic_nodes=original_logic_nodes,
                chapter_blueprint=chapter_blueprint,
                chapter_outline=chapter_outline,
                pre_chapter_summary=pre_chapter_summary,
                cumulative_substory_summary=cumulative_substory_summary,
                previous_scene_chunk=previous_scene_chunk or SceneChunkSchema(content=""),
            )
        )
        return written_chapter

    async def get(self, written_chapter_id: str) -> WrittenChapterSchema | None:
        async with self.uow_factory() as uow:
            written_chapter = await uow.writing.written_chapters.get(written_chapter_id)
            if written_chapter is None:
                return None
            return self._to_schema(written_chapter)

    async def get_latest_by_bible(self, bible_id: str) -> WrittenChapterSchema | None:
        async with self.uow_factory() as uow:
            written_chapter = await uow.writing.written_chapters.get_latest_chapter(bible_id)
            if written_chapter is None:
                return None
            return self._to_schema(written_chapter)

    async def get_latest_by_substory(self, substory_id: str) -> WrittenChapterSchema | None:
        async with self.uow_factory() as uow:
            written_chapter = await uow.writing.written_chapters.get_latest_chapter_by_substory(
                substory_id
            )
            if written_chapter is None:
                return None
            return self._to_schema(written_chapter)
