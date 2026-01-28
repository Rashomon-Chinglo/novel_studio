from ..chain.chapter import get_blueprint_chain, get_brainstorm_chain, get_chapter_chain
from ..schemas.chapter import Chapter, ChapterBlueprint
from ..schemas.substory import Substory


class ChapterEngine:
    def __init__(self, substory: Substory):
        self.brainstorm_llm = get_brainstorm_chain()
        self.blueprint_llm = get_blueprint_chain()
        self.chapter_llm = get_chapter_chain()

    async def blueprint_init(self):
        pass

    async def brainstorm(self, history: list[str], user_input: str):
        pass

    async def blueprint_generate(self, messages: list[str]) -> ChapterBlueprint:
        pass

    async def generate(self, messages: list[str]) -> Chapter:
        pass
