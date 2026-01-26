from app.modules.base.prompt import PromptTemplate
from .context import MaterialsMiningContext
from langchain_core.prompts import ChatPromptTemplate


class MaterialsMiningPrompt(PromptTemplate[MaterialsMiningContext]):
    @property
    def template(self) -> str:
        return """
        你是一位资深小说编辑。你的任务是从文本中**挖掘 (Mine)** 出高价值的素材片段。

        规则：
        1. 输入是一段约 500 字的小说原文。
        2. 你需要摘录出 0-N 个“精华片段” (ExtractedSnippet)。
        3. 每个片段 20-100 字，必须是原文摘录。
        4. 如果没有精彩内容，返回空列表。
        
        【文本片段】
        {text}
        
        """

    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
            ]
        )

    def build_variables(self, context: MaterialsMiningContext) -> dict[str, str]:
        return {
            "text": context.text,
        }

    def version(self) -> str:
        return "1.0.0"
