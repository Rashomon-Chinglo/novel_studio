from langchain_text_splitters import RecursiveCharacterTextSplitter

from .chain import get_mining_chain
from .context import MaterialsMiningContext
from .prompt import MaterialsMiningPrompt
from .schemas import ExtractedResult


class MaterialEngine:
    MaterialsMiningContext = MaterialsMiningContext

    def __init__(self):
        self.material_mining_prompt = MaterialsMiningPrompt()
        self.llm = get_mining_chain(self.material_mining_prompt.prompt)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=20,
            separators=["\n\n", "\n", "。", "！", "？"],
            length_function=len,
        )

    def split_text(self, text: str) -> list[str]:
        return self.splitter.split_text(text)

    async def mine(self, context: MaterialsMiningContext) -> ExtractedResult:
        variables = self.material_mining_prompt.build_variables(context)
        return await self.llm.ainvoke(variables)
