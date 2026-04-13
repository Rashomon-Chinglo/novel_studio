from collections.abc import Callable

from app.modules.outlines.engines import SubstoryEngine
from app.modules.outlines.schemas import Bible as BibleSchema
from app.modules.outlines.schemas import Substory as SubstorySchema
from app.persistence import SqlAlchemyUnitOfWork
from app.persistence.models import Substory


class SubstoryService:
    def __init__(
        self,
        uow_factory: Callable[[], SqlAlchemyUnitOfWork] = SqlAlchemyUnitOfWork,
        engine_factory: Callable[[], SubstoryEngine] = SubstoryEngine,
    ) -> None:
        self.uow_factory: Callable[[], SqlAlchemyUnitOfWork] = uow_factory
        self.engine: SubstoryEngine = engine_factory()

    def _to_schema(self, model: Substory) -> SubstorySchema:
        return SubstorySchema(**model.content)

    async def get(self, *, substory_id: str) -> SubstorySchema:
        async with self.uow_factory() as uow:
            substory = await uow.outlines.substories.get(substory_id)
            if substory is None:
                raise ValueError(f"Substory with id {substory_id} not found.")
            return self._to_schema(substory)

    async def create(
        self,
        *,
        bible_id: str,
        order_index: int,
        substory: SubstorySchema,
    ) -> str:
        async with self.uow_factory() as uow:
            model = Substory(
                bible_id=bible_id,
                title=substory.substory_title,
                order_index=order_index,
                content=substory.model_dump(),
            )
            uow.outlines.substories.add(model)
            await uow.commit()
            return model.id

    async def brainstorm(
        self,
        *,
        history: list[str],
        user_input: str,
        bible: BibleSchema,
    ) -> str:
        return await self.engine.brainstorm(
            SubstoryEngine.SubstoryBrainstormContext(
                history=history,
                user_input=user_input,
                bible=bible,
            )
        )

    async def generate(self, *, bible: BibleSchema, messages: list[str]) -> SubstorySchema:
        return await self.engine.generate(
            SubstoryEngine.SubstoryGenerateContext(bible=bible, messages=messages)
        )

    async def list_by_bible(self, *, bible_id: str) -> list[SubstorySchema]:
        async with self.uow_factory() as uow:
            substories = await uow.outlines.substories.list_by_bible(bible_id)
            return [self._to_schema(substory) for substory in substories]
