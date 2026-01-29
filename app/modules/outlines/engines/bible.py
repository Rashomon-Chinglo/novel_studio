from ..chain.bible import get_bible_chain, get_brainstorm_chain
from ..context.bible import BibleBrainstormContext, BibleGenerateContext
from ..prompts.bible import BibleBrainstormPrompt, BibleGeneratePrompt
from ..schemas import Bible


class BibleEngine:
    BibleBrainstormContext = BibleBrainstormContext
    BibleGenerateContext = BibleGenerateContext

    def __init__(self):
        self.brainstorm_template = BibleBrainstormPrompt()
        self.brainstorm_llm = get_brainstorm_chain(self.brainstorm_template.prompt)

        self.bible_template = BibleGeneratePrompt()
        self.bible_llm = get_bible_chain(self.bible_template.prompt)

    async def brainstorm(self, context: BibleBrainstormContext) -> str:
        variables = self.brainstorm_template.build_variables(context)
        result = await self.brainstorm_llm.ainvoke(variables)
        return result

    async def generate(self, context: BibleGenerateContext) -> Bible:
        variables = self.bible_template.build_variables(context)
        result = await self.bible_llm.ainvoke(variables)
        return result
