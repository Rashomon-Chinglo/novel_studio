from langchain_core.prompts import ChatPromptTemplate

from app.modules.base.prompt import PromptTemplate

from .context import MaterialsMiningContext


class MaterialsMiningPrompt(PromptTemplate[MaterialsMiningContext]):
    @property
    def template(self) -> str:
        return """
        <角色>
        你是一位资深小说编辑，擅长从文本中挖掘高价值的素材片段。
        </角色>

        <任务>
        从给定的小说原文中摘录出精华片段 (ExtractedSnippet)。
        </任务>

        <文本片段>
        {text}
        </文本片段>

        <创作要求>
        1. 输入是一段约 500 字的小说原文
        2. 摘录出 0-N 个"精华片段"
        3. 每个片段 20-100 字，必须是原文摘录
        4. 如果没有精彩内容，返回空列表
        </创作要求>

        <输出字段说明>
        返回一个精华片段列表 (snippets)，每个片段 (MaterialSnippet) 包含以下字段：

        - essential_text (精华文本): 从文章中摘录的精华文本，20-100字，必须是原文摘录
        - category (分类): 摘录文本的分类，如"环境描写"、"人物对话"、"心理活动"、"动作场面"等
        - tags (标签): 摘录文本的标签列表，用于细化分类，如["雨夜", "孤独"]
        - mood (情绪): 摘录文本的情绪基调，如"悲伤"、"紧张"、"温馨"、"压抑"等
        </输出字段说明>
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
