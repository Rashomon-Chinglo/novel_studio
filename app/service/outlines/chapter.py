from collections.abc import Callable

from app.modules.base import ChapterSummary, CumulativeSubstorySummary
from app.modules.outlines.engines import ChapterEngine
from app.modules.outlines.schemas import Bible as BibleSchema
from app.modules.outlines.schemas import (
    ChapterBlueprint as ChapterBlueprintSchema,
)
from app.modules.outlines.schemas import ChapterOriginalSubstoryNodes
from app.modules.outlines.schemas import (
    ChapterOutline as ChapterOutlineSchema,
)
from app.modules.outlines.schemas import Substory as SubstorySchema
from app.persistence import SqlAlchemyUnitOfWork
from app.persistence.models import ChapterBlueprint, ChapterOutline


class ChapterService:
    def __init__(
        self,
        uow_factory: Callable[[], SqlAlchemyUnitOfWork] = SqlAlchemyUnitOfWork,
        engine_factory: Callable[[], ChapterEngine] = ChapterEngine,
    ) -> None:
        self.uow_factory: Callable[[], SqlAlchemyUnitOfWork] = uow_factory
        self.engine: ChapterEngine = engine_factory()

    def _to_blueprint_schema(self, model: ChapterBlueprint) -> ChapterBlueprintSchema:
        return ChapterBlueprintSchema(**model.content)

    def _to_outline_schema(self, model: ChapterOutline) -> ChapterOutlineSchema:
        return ChapterOutlineSchema(**model.content)

    async def get_blueprint(self, *, chapter_blueprint_id: str) -> ChapterBlueprintSchema:
        async with self.uow_factory() as uow:
            chapter_blueprint = await uow.outlines.chapter_blueprints.get(chapter_blueprint_id)
            if chapter_blueprint is None:
                raise ValueError(f"Chapter blueprint with id {chapter_blueprint_id} not found.")
            return self._to_blueprint_schema(chapter_blueprint)

    async def get_outline(self, *, chapter_outline_id: str) -> ChapterOutlineSchema:
        async with self.uow_factory() as uow:
            chapter_outline = await uow.outlines.chapter_outlines.get(chapter_outline_id)
            if chapter_outline is None:
                raise ValueError(f"Chapter outline with id {chapter_outline_id} not found.")
            return self._to_outline_schema(chapter_outline)

    async def create_blueprint(
        self,
        *,
        substory_id: str,
        bible_id: str,
        chapter_index: int,
        substory_chapter_index: int,
        workflow_run_id: str,
        chapter_blueprint: ChapterBlueprintSchema,
    ) -> str:
        async with self.uow_factory() as uow:
            model = ChapterBlueprint(
                content=chapter_blueprint.model_dump(),
                substory_id=substory_id,
                bible_id=bible_id,
                chapter_index=chapter_index,
                substory_chapter_index=substory_chapter_index,
                workflow_run_id=workflow_run_id,
            )
            uow.outlines.chapter_blueprints.add(model)
            await uow.commit()
            return model.id

    async def create_outline(
        self, *, chapter_blueprint_id: str, chapter_outline: ChapterOutlineSchema
    ) -> str:
        async with self.uow_factory() as uow:
            chapter_blueprint = await uow.outlines.chapter_blueprints.get(chapter_blueprint_id)
            if chapter_blueprint is None:
                raise ValueError(f"Chapter blueprint with id {chapter_blueprint_id} not found.")
            model = ChapterOutline(
                content=chapter_outline.model_dump(),
                substory_id=chapter_blueprint.substory_id,
                bible_id=chapter_blueprint.bible_id,
                chapter_index=chapter_blueprint.chapter_index,
                substory_chapter_index=chapter_blueprint.substory_chapter_index,
                workflow_run_id=chapter_blueprint.workflow_run_id,
                chapter_blueprint_id=chapter_blueprint_id,
            )
            uow.outlines.chapter_outlines.add(model)
            await uow.commit()
            return model.id

    async def generate_blueprint(
        self,
        *,
        bible: BibleSchema,
        substory: SubstorySchema,
        cumulative_substory_summary: CumulativeSubstorySummary | None,
        pre_chapter_summary: ChapterSummary | None,
        logic_nodes_to_process: ChapterOriginalSubstoryNodes,
    ) -> ChapterBlueprintSchema:
        return await self.engine.chapter_blueprint_generate(
            ChapterEngine.ChapterBlueprintContext(
                bible=bible,
                substory=substory,
                cumulative_substory_summary=cumulative_substory_summary
                or CumulativeSubstorySummary(summary=""),
                pre_chapter_summary=pre_chapter_summary or ChapterSummary(summary=""),
                logic_nodes_to_process=logic_nodes_to_process,
            )
        )

    async def generate_outline(
        self,
        *,
        bible: BibleSchema,
        substory: SubstorySchema,
        cumulative_substory_summary: CumulativeSubstorySummary | None,
        pre_chapter_summary: ChapterSummary | None,
        logic_nodes_to_process: ChapterOriginalSubstoryNodes,
        chapter_blueprint: ChapterBlueprintSchema,
    ) -> ChapterOutlineSchema:
        return await self.engine.chapter_generate(
            ChapterEngine.ChapterContext(
                bible=bible,
                substory=substory,
                cumulative_substory_summary=cumulative_substory_summary
                or CumulativeSubstorySummary(summary=""),
                pre_chapter_summary=pre_chapter_summary or ChapterSummary(summary=""),
                logic_nodes_to_process=logic_nodes_to_process,
                chapter_blueprint=chapter_blueprint,
            )
        )

    async def get_latest_outline(self, *, bible_id: str) -> ChapterOutlineSchema | None:
        async with self.uow_factory() as uow:
            chapter_outline = await uow.outlines.chapter_outlines.get_latest(bible_id)
            if chapter_outline is None:
                return None
            return self._to_outline_schema(chapter_outline)

    async def get_latest_blueprint(self, *, bible_id: str) -> ChapterBlueprintSchema | None:
        async with self.uow_factory() as uow:
            chapter_blueprint = await uow.outlines.chapter_blueprints.get_latest(bible_id)
            if chapter_blueprint is None:
                return None
            return self._to_blueprint_schema(chapter_blueprint)

    async def list_blueprint_by_substory(self, *, substory_id: str) -> list[ChapterBlueprintSchema]:
        async with self.uow_factory() as uow:
            chapter_blueprints = await uow.outlines.chapter_blueprints.list_by_substory(substory_id)
            return [
                self._to_blueprint_schema(chapter_blueprint)
                for chapter_blueprint in chapter_blueprints
            ]

    async def list_outline_by_substory(self, *, substory_id: str) -> list[ChapterOutlineSchema]:
        async with self.uow_factory() as uow:
            chapter_outlines = await uow.outlines.chapter_outlines.list_by_substory(substory_id)
            return [
                self._to_outline_schema(chapter_outline) for chapter_outline in chapter_outlines
            ]
