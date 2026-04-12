from dataclasses import dataclass, field
from datetime import datetime

from app.domain import WorkflowErrorCode, WorkflowStage, WorkflowStatus
from app.modules.base import ChapterSummary, CumulativeSubstorySummary
from app.modules.outlines.schemas import (
    Bible,
    ChapterBlueprint,
    ChapterOriginalSubstoryNodes,
    ChapterOutline,
    Substory,
    SubstoryActionNode,
)
from app.modules.writing import SceneChunk, WrittenChapter
from app.persistence.models.workflow import WorkflowRun
from app.service import PostWritingService, WorkflowRunService, WritingService
from app.service.material_providers import NoopMaterialProvider
from app.service.outlines import OutlineServiceGroup


@dataclass(slots=True)
class ContextArtifacts:
    chapter_blueprint_id: str | None = None
    chapter_outline_id: str | None = None
    written_chapter_id: str | None = None
    chapter_summary_id: str | None = None
    cumulative_substory_summary_id: str | None = None


@dataclass(slots=True)
class ChapterOrchestratorRunContext:
    run: WorkflowRun
    bible: Bible
    substory: Substory
    pre_cumulative_substory_summary: CumulativeSubstorySummary
    pre_chapter_summary: ChapterSummary
    pre_scene_chunk: SceneChunk
    logic_nodes_to_process: ChapterOriginalSubstoryNodes
    context_artifacts: ContextArtifacts = field(default_factory=ContextArtifacts)
    chapter_summary: ChapterSummary | None = None
    cumulative_substory_summary: CumulativeSubstorySummary | None = None
    chapter_blueprint: ChapterBlueprint | None = None
    chapter_outline: ChapterOutline | None = None
    written_chapter: WrittenChapter | None = None


@dataclass(slots=True)
class ChapterOrchestratorStatus:
    id: str
    status: WorkflowStatus
    current_stage: WorkflowStage
    bible_id: str
    substory_id: str
    chapter_index: int
    substory_chapter_index: int
    error_code: WorkflowErrorCode | None
    error_message: str | None
    started_at: datetime
    finished_at: datetime | None


class ChapterOrchestrator:
    def __init__(self) -> None:
        self.workflow_run_service: WorkflowRunService = WorkflowRunService()
        self.writing_service: WritingService = WritingService(
            material_provider=NoopMaterialProvider()
        )
        self.post_writing_service: PostWritingService = PostWritingService()
        self.outlines: OutlineServiceGroup = OutlineServiceGroup()

    async def start(
        self,
        *,
        bible_id: str,
        substory_id: str,
        chapter_index: int,
        substory_chapter_index: int,
    ) -> str:
        run = await self.workflow_run_service.create(
            bible_id=bible_id,
            substory_id=substory_id,
            chapter_index=chapter_index,
            substory_chapter_index=substory_chapter_index,
        )
        await self._run_to_completion(run)
        return run.id

    async def get_status(
        self,
        run_id: str,
    ) -> ChapterOrchestratorStatus:
        run = await self.workflow_run_service.get(run_id)
        if run is None:
            raise ValueError(f"Workflow run {run_id} not found.")
        return ChapterOrchestratorStatus(
            id=run.id,
            status=run.status,
            current_stage=run.current_stage,
            bible_id=run.bible_id,
            substory_id=run.substory_id,
            chapter_index=run.chapter_index,
            substory_chapter_index=run.substory_chapter_index,
            error_code=run.error_code,
            error_message=run.error_message,
            started_at=run.started_at,
            finished_at=run.finished_at,
        )

    def _get_logic_nodes(
        self, *, logic_nodes: list[SubstoryActionNode], substory_chapter_index: int
    ) -> ChapterOriginalSubstoryNodes:
        try:
            assert substory_chapter_index > 0
            return ChapterOriginalSubstoryNodes(nodes=[logic_nodes[substory_chapter_index - 1]])
        except IndexError as e:
            raise ValueError(
                f"Substory chapter index {substory_chapter_index} is out of range for logic nodes."
            ) from e
        except AssertionError as e:
            raise ValueError(
                f"Substory chapter index {substory_chapter_index} must be positive."
            ) from e

    async def _load_context(self, run: WorkflowRun) -> ChapterOrchestratorRunContext:
        bible = await self.outlines.bible.get(bible_id=run.bible_id)
        substory = await self.outlines.substory.get(substory_id=run.substory_id)
        logic_nodes_to_process = self._get_logic_nodes(
            logic_nodes=substory.logic_nodes,
            substory_chapter_index=run.substory_chapter_index,
        )

        pre_written_chapter = await self.writing_service.get_latest_by_bible(run.bible_id)
        pre_scene_chunk = (
            pre_written_chapter.chunks[-1] if pre_written_chapter else SceneChunk(content="")
        )

        pre_chapter_summary = await self.post_writing_service.get_latest_chapter_summary(
            bible_id=run.bible_id
        )
        pre_chapter_summary = pre_chapter_summary or ChapterSummary(summary="")

        pre_cumulative_substory_summary = (
            await self.post_writing_service.get_latest_cumulative_substory_summary(
                bible_id=run.bible_id
            )
        )
        pre_cumulative_substory_summary = (
            pre_cumulative_substory_summary or CumulativeSubstorySummary(summary="")
        )

        return ChapterOrchestratorRunContext(
            run=run,
            bible=bible,
            substory=substory,
            pre_cumulative_substory_summary=pre_cumulative_substory_summary,
            pre_chapter_summary=pre_chapter_summary,
            pre_scene_chunk=pre_scene_chunk,
            logic_nodes_to_process=logic_nodes_to_process,
        )

    async def _generate_blueprint(self, ctx: ChapterOrchestratorRunContext) -> None:
        chapter_blueprint = await self.outlines.chapter.generate_blueprint(
            bible=ctx.bible,
            substory=ctx.substory,
            cumulative_substory_summary=ctx.pre_cumulative_substory_summary,
            pre_chapter_summary=ctx.pre_chapter_summary,
            logic_nodes_to_process=ctx.logic_nodes_to_process,
        )

        chapter_blueprint_id = await self.outlines.chapter.create_blueprint(
            substory_id=ctx.run.substory_id,
            bible_id=ctx.run.bible_id,
            chapter_index=ctx.run.chapter_index,
            substory_chapter_index=ctx.run.substory_chapter_index,
            workflow_run_id=ctx.run.id,
            chapter_blueprint=chapter_blueprint,
        )

        ctx.chapter_blueprint = chapter_blueprint
        ctx.context_artifacts.chapter_blueprint_id = chapter_blueprint_id

    async def _generate_outline(self, ctx: ChapterOrchestratorRunContext) -> None:
        if ctx.chapter_blueprint is None:
            raise ValueError("Chapter blueprint is not available.")
        if ctx.context_artifacts.chapter_blueprint_id is None:
            raise ValueError("Chapter blueprint id is not available.")

        chapter_outline = await self.outlines.chapter.generate_outline(
            bible=ctx.bible,
            substory=ctx.substory,
            cumulative_substory_summary=ctx.pre_cumulative_substory_summary,
            pre_chapter_summary=ctx.pre_chapter_summary,
            logic_nodes_to_process=ctx.logic_nodes_to_process,
            chapter_blueprint=ctx.chapter_blueprint,
        )

        chapter_outline_id = await self.outlines.chapter.create_outline(
            chapter_blueprint_id=ctx.context_artifacts.chapter_blueprint_id,
            chapter_outline=chapter_outline,
        )
        ctx.chapter_outline = chapter_outline
        ctx.context_artifacts.chapter_outline_id = chapter_outline_id

    async def _generate_writing(self, ctx: ChapterOrchestratorRunContext) -> None:
        if ctx.chapter_blueprint is None:
            raise ValueError("Chapter blueprint is not available.")
        if ctx.chapter_outline is None:
            raise ValueError("Chapter outline is not available.")
        if ctx.context_artifacts.chapter_outline_id is None:
            raise ValueError("Chapter outline id is not available.")

        written_chapter = await self.writing_service.generate(
            bible=ctx.bible,
            substory=ctx.substory,
            cumulative_substory_summary=ctx.pre_cumulative_substory_summary,
            pre_chapter_summary=ctx.pre_chapter_summary,
            chapter_blueprint=ctx.chapter_blueprint,
            chapter_outline=ctx.chapter_outline,
            original_logic_nodes=ctx.logic_nodes_to_process,
            previous_scene_chunk=ctx.pre_scene_chunk,
        )

        written_chapter_id = await self.writing_service.create(
            chapter_outline_id=ctx.context_artifacts.chapter_outline_id,
            written_chapter=written_chapter,
        )

        ctx.written_chapter = written_chapter
        ctx.context_artifacts.written_chapter_id = written_chapter_id

    async def _generate_chapter_summary(self, ctx: ChapterOrchestratorRunContext) -> None:
        if ctx.written_chapter is None:
            raise ValueError("Written chapter is not available.")
        if ctx.context_artifacts.written_chapter_id is None:
            raise ValueError("Written chapter id is not available.")
        if ctx.chapter_outline is None:
            raise ValueError("Chapter outline is not available.")

        chapter_summary = await self.post_writing_service.summarize_chapter(
            bible=ctx.bible,
            substory=ctx.substory,
            original_logic_nodes=ctx.logic_nodes_to_process,
            pre_chapter_summary=ctx.pre_chapter_summary,
            chapter_outline=ctx.chapter_outline,
            written_chapter=ctx.written_chapter,
            pre_cumulative_substory_summary=ctx.pre_cumulative_substory_summary,
        )
        chapter_summary_id = await self.post_writing_service.create_chapter_summary(
            written_chapter_id=ctx.context_artifacts.written_chapter_id,
            chapter_summary_content=chapter_summary.summary,
        )

        ctx.chapter_summary = chapter_summary
        ctx.context_artifacts.chapter_summary_id = chapter_summary_id

    async def _generate_cumulative_substory_summary(
        self, ctx: ChapterOrchestratorRunContext
    ) -> None:
        if ctx.context_artifacts.written_chapter_id is None:
            raise ValueError("Written chapter id is not available.")
        if ctx.chapter_summary is None:
            raise ValueError("Chapter summary is not available.")

        cumulative_summary = await self.post_writing_service.summarize_cumulative_substory(
            bible=ctx.bible,
            substory=ctx.substory,
            pre_cumulative_substory_summary=ctx.pre_cumulative_substory_summary,
            current_chapter_summary=ctx.chapter_summary,
        )
        cumulative_summary_id = await self.post_writing_service.create_cumulative_substory_summary(
            written_chapter_id=ctx.context_artifacts.written_chapter_id,
            content=cumulative_summary.summary,
        )

        ctx.cumulative_substory_summary = cumulative_summary
        ctx.context_artifacts.cumulative_substory_summary_id = cumulative_summary_id

    async def _run_to_completion(
        self,
        run: WorkflowRun,
    ) -> None:
        try:
            run_id = run.id
            await self.workflow_run_service.mark_stage(run_id, WorkflowStage.LOAD_CONTEXT)
            ctx = await self._load_context(run)
            await self.workflow_run_service.mark_stage(run_id, WorkflowStage.GENERATE_BLUEPRINT)
            await self._generate_blueprint(ctx)
            await self.workflow_run_service.mark_stage(run_id, WorkflowStage.GENERATE_OUTLINE)
            await self._generate_outline(ctx)
            await self.workflow_run_service.mark_stage(run_id, WorkflowStage.GENERATE_WRITING)
            await self._generate_writing(ctx)
            await self.workflow_run_service.mark_stage(run_id, WorkflowStage.GENERATE_SUMMARY)
            await self._generate_chapter_summary(ctx)
            await self.workflow_run_service.mark_stage(
                run_id, WorkflowStage.GENERATE_CUMULATIVE_SUMMARY
            )
            await self._generate_cumulative_substory_summary(ctx)
            await self.workflow_run_service.mark_succeeded(run_id)
        except Exception as e:
            await self.workflow_run_service.mark_failed(
                run_id, WorkflowErrorCode.LLM_CALL_ERROR, str(e)
            )

    async def resume(
        self,
        run_id: str,
    ):
        raise NotImplementedError

    async def submit_review(
        self,
        run_id: str,
    ):
        raise NotImplementedError
