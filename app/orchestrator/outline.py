from app.modules.outlines.schemas import Bible, Substory
from app.service.outlines import BibleService, SubstoryService


class OutlineOrchestrator:
    def __init__(
        self,
        bible_service: BibleService | None = None,
        substory_service: SubstoryService | None = None,
    ) -> None:
        self.bible_service: BibleService = bible_service or BibleService()
        self.substory_service: SubstoryService = substory_service or SubstoryService()

    async def create_bible(self, *, messages: list[str]) -> str:
        bible = await self.bible_service.generate(messages=messages)
        return await self.bible_service.create(bible=bible)

    async def get_bible(self, *, bible_id: str) -> Bible:
        return await self.bible_service.get(bible_id=bible_id)

    async def create_substory(
        self,
        *,
        bible_id: str,
        substory_order_index: int,
        messages: list[str],
    ) -> str:
        bible = await self.bible_service.get(bible_id=bible_id)
        substory = await self.substory_service.generate(bible=bible, messages=messages)
        return await self.substory_service.create(
            bible_id=bible_id,
            order_index=substory_order_index,
            substory=substory,
        )

    async def get_substory(self, *, substory_id: str) -> Substory:
        return await self.substory_service.get(substory_id=substory_id)

    async def brainstorm_bible(self, *, history: list[str], user_input: str) -> str:
        return await self.bible_service.brainstorm(history=history, user_input=user_input)

    async def brainstorm_substory(
        self,
        *,
        history: list[str],
        user_input: str,
        bible_id: str,
    ) -> str:
        bible = await self.bible_service.get(bible_id=bible_id)
        return await self.substory_service.brainstorm(
            history=history,
            user_input=user_input,
            bible=bible,
        )
