from collections.abc import Callable

from app.modules.base import ChapterSummary as ChapterSummarySchema
from app.modules.base import CumulativeSubstorySummary as CumulativeSubstorySummarySchema
from app.modules.outlines.schemas import (
    Bible,
    ChapterOriginalSubstoryNodes,
    ChapterOutline,
    Substory,
)
from app.modules.post_writing.engine import PostWritingEngine
from app.modules.writing.schemas import WrittenChapter
from app.persistence import SqlAlchemyUnitOfWork
from app.persistence.models import ChapterSummary, CumulativeSubstorySummary


class PostWritingService:
    def __init__(
        self, uow_factory: Callable[[], SqlAlchemyUnitOfWork] = SqlAlchemyUnitOfWork
    ) -> None:
        self.uow_factory: Callable[[], SqlAlchemyUnitOfWork] = uow_factory
        self.engine: PostWritingEngine = PostWritingEngine()

    def _to_chapter_summary_schema(self, model: ChapterSummary) -> ChapterSummarySchema:
        return ChapterSummarySchema(
            summary=model.content,
        )

    def _to_cumulative_substory_summary_schema(
        self, model: CumulativeSubstorySummary
    ) -> CumulativeSubstorySummarySchema:
        return CumulativeSubstorySummarySchema(
            summary=model.content,
        )

    async def summarize_chapter(
        self,
        *,
        bible: Bible,
        substory: Substory,
        original_logic_nodes: ChapterOriginalSubstoryNodes,
        chapter_outline: ChapterOutline,
        pre_chapter_summary: ChapterSummarySchema,
        written_chapter: WrittenChapter,
        pre_cumulative_substory_summary: CumulativeSubstorySummarySchema,
    ) -> ChapterSummarySchema:
        return await self.engine.chapter_summary(
            self.engine.ChapterSummaryContext(
                bible=bible,
                substory=substory,
                original_logic_nodes=original_logic_nodes,
                chapter_outline=chapter_outline,
                cumulative_substory_summary=pre_cumulative_substory_summary,
                pre_chapter_summary=pre_chapter_summary,
                written_chapter=written_chapter,
            )
        )

    async def summarize_cumulative_substory(
        self,
        *,
        bible: Bible,
        substory: Substory,
        pre_cumulative_substory_summary: CumulativeSubstorySummarySchema,
        current_chapter_summary: ChapterSummarySchema,
    ) -> CumulativeSubstorySummarySchema:
        return await self.engine.cumulative_substory_summary(
            self.engine.SubstoryCumulativeSummaryContext(
                bible=bible,
                substory=substory,
                cumulative_substory_summary=pre_cumulative_substory_summary,
                current_chapter_summary=current_chapter_summary,
            )
        )

    async def save_chapter_summary(
        self,
        *,
        chapter_summary_content: str,
        written_chapter_id: str,
    ) -> str:
        async with self.uow_factory() as uow:
            written_chapter = await uow.writing.written_chapters.get(written_chapter_id)
            if written_chapter is None:
                raise ValueError(f"Written chapter with id {written_chapter_id} not found.")

            summary = ChapterSummary(
                bible_id=written_chapter.bible_id,
                substory_id=written_chapter.substory_id,
                chapter_index=written_chapter.chapter_index,
                written_chapter_id=written_chapter_id,
                workflow_run_id=written_chapter.workflow_run_id,
                content=chapter_summary_content,
            )
            uow.post_writing.chapter_summaries.add(summary)

            await uow.commit()

            return summary.id

    async def save_cumulative_substory_summary(
        self,
        *,
        written_chapter_id: str,
        content: str,
    ) -> str:
        async with self.uow_factory() as uow:
            written_chapter = await uow.writing.written_chapters.get(written_chapter_id)
            if written_chapter is None:
                raise ValueError(f"Written chapter with id {written_chapter_id} not found.")
            summary = CumulativeSubstorySummary(
                bible_id=written_chapter.bible_id,
                substory_id=written_chapter.substory_id,
                chapter_index=written_chapter.chapter_index,
                written_chapter_id=written_chapter_id,
                workflow_run_id=written_chapter.workflow_run_id,
                content=content,
            )
            uow.post_writing.cumulative_substory_summaries.add(summary)

            await uow.commit()
            return summary.id

    async def get_latest_cumulative_substory_summary(
        self,
        *,
        bible_id: str,
    ) -> CumulativeSubstorySummarySchema | None:
        async with self.uow_factory() as uow:
            summary = await uow.post_writing.cumulative_substory_summaries.get_latest_by_bible(
                bible_id
            )
            if summary is None:
                return None
            return self._to_cumulative_substory_summary_schema(summary)

    async def get_latest_chapter_summary(
        self,
        *,
        bible_id: str,
    ) -> ChapterSummarySchema | None:
        async with self.uow_factory() as uow:
            summary = await uow.post_writing.chapter_summaries.get_latest_by_bible(bible_id)
            if summary is None:
                return None
            return self._to_chapter_summary_schema(summary)

    async def get_substory_latest_summary(
        self,
        *,
        substory_id: str,
    ) -> CumulativeSubstorySummarySchema | None:
        async with self.uow_factory() as uow:
            summary = await uow.post_writing.cumulative_substory_summaries.get_latest_by_substory(
                substory_id
            )
            if summary is None:
                return None
            return self._to_cumulative_substory_summary_schema(summary)
