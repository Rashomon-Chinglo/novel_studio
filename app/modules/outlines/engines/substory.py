from ..schemas.bible import Bible
from ..schemas.substory import Substory
from ..chain.substory import get_brainstorm_chain
from ..chain.substory import get_substory_chain
from ..context.substory import BrainstormContext
from ..context.substory import SubstoryContext
from ..prompts.substory import BrainstormPrompt
from ..prompts.substory import SubstoryPrompt


class SubstoryEngine:
    def __init__(self, bible: Bible):
        self.bible = bible
        self.brainstorm_template = BrainstormPrompt()
        self.brainstorm_llm = get_brainstorm_chain(self.brainstorm_template.prompt)

        self.substory_template = SubstoryPrompt()
        self.substory_llm = get_substory_chain(self.substory_template.prompt)

    async def brainstorm(self, history: list[str], user_input: str) -> str:
        context = BrainstormContext(
            history=history, user_input=user_input, bible=self.bible
        )
        variables = self.brainstorm_template.build_variables(context)
        result = await self.brainstorm_llm.ainvoke(variables)
        return result

    async def generate(self, history: list[str]) -> Substory:
        context = SubstoryContext(history=history, bible=self.bible)
        variables = self.substory_template.build_variables(context)
        result = await self.substory_llm.ainvoke(variables)
        return result
