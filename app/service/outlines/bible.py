from collections.abc import Callable

from app.modules.outlines.engines import BibleEngine
from app.modules.outlines.schemas import Bible as BibleSchema
from app.persistence import SqlAlchemyUnitOfWork
from app.persistence.models import Bible


class BibleService:
    def __init__(
        self,
        uow_factory: Callable[[], SqlAlchemyUnitOfWork] = SqlAlchemyUnitOfWork,
        engine_factory: Callable[[], BibleEngine] = BibleEngine,
    ) -> None:
        self.uow_factory: Callable[[], SqlAlchemyUnitOfWork] = uow_factory
        self.engine: BibleEngine = engine_factory()

    def _to_schema(self, model: Bible) -> BibleSchema:
        return BibleSchema(**model.content)

    async def get(self, *, bible_id: str) -> BibleSchema:
        async with self.uow_factory() as uow:
            bible = await uow.outlines.bibles.get(bible_id)
            if bible is None:
                raise ValueError(f"Bible with id {bible_id} not found.")
            return self._to_schema(bible)

    async def create(self, *, bible: BibleSchema) -> str:
        async with self.uow_factory() as uow:
            model = Bible(content=bible.model_dump())
            uow.outlines.bibles.add(model)
            await uow.commit()
            return model.id

    async def brainstorm(self, *, history: list[str], user_input: str) -> str:
        return await self.engine.brainstorm(
            BibleEngine.BibleBrainstormContext(history=history, user_input=user_input)
        )

    async def generate(self, *, messages: list[str]) -> BibleSchema:
        return await self.engine.generate(BibleEngine.BibleGenerateContext(messages=messages))

    async def list(self) -> list[BibleSchema]:
        async with self.uow_factory() as uow:
            bibles = await uow.outlines.bibles.list_all()
            return [self._to_schema(bible) for bible in bibles]
