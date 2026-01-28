from ..chain.bible import get_bible_chain, get_brainstorm_chain
from ..context.bible import BibleContext, BrainstormContext
from ..prompts.bible import BiblePrompt, BrainstormPrompt
from ..schemas import Bible


class BibleEngine:
    def __init__(self):
        self.brainstorm_template = BrainstormPrompt()
        self.brainstorm_llm = get_brainstorm_chain(self.brainstorm_template.prompt)

        self.bible_template = BiblePrompt()
        self.bible_llm = get_bible_chain(self.bible_template.prompt)

    async def brainstorm(self, history: list[str], user_input: str) -> str:
        context = BrainstormContext(history=history, user_input=user_input)
        variables = self.brainstorm_template.build_variables(context)
        result = await self.brainstorm_llm.ainvoke(variables)
        return result

    async def generate(self, messages: list[str]) -> Bible:
        context = BibleContext(messages=messages)
        variables = self.bible_template.build_variables(context)
        result = await self.bible_llm.ainvoke(variables)
        return result
