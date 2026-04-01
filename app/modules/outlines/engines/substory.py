from ..chain import get_substory_brainstorm_chain, get_substory_chain
from ..context import SubstoryBrainstormContext, SubstoryGenerateContext
from ..prompts import SubstoryBrainstormPrompt, SubstoryGeneratePrompt
from ..schemas import Substory


class SubstoryEngine:
    SubstoryBrainstormContext = SubstoryBrainstormContext
    SubstoryGenerateContext = SubstoryGenerateContext

    def __init__(self):
        self.brainstorm_template = SubstoryBrainstormPrompt()
        self.brainstorm_llm = get_substory_brainstorm_chain(self.brainstorm_template.prompt)

        self.substory_template = SubstoryGeneratePrompt()
        self.substory_llm = get_substory_chain(self.substory_template.prompt)

    async def brainstorm(self, context: SubstoryBrainstormContext) -> str:
        variables = self.brainstorm_template.build_variables(context)
        result = await self.brainstorm_llm.ainvoke(variables)
        return result

    async def generate(self, context: SubstoryGenerateContext) -> Substory:
        variables = self.substory_template.build_variables(context)
        result = await self.substory_llm.ainvoke(variables)
        return result
