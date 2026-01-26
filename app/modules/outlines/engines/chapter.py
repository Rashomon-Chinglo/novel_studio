from ..schemas.chapter import ChapterBlueprint, Chapter
from ..schemas.substory import Substory, SubstoryActionNode
from ..chain.chapter import get_brainstorm_chain, get_blueprint_chain, get_chapter_chain


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
