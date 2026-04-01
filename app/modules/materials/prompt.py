from langchain_core.prompts import ChatPromptTemplate

from app.modules.base import PromptTemplate

from .context import MaterialsMiningContext


class MaterialsMiningPrompt(PromptTemplate[MaterialsMiningContext]):
    @property
    def template(self) -> str:
        return """
<角色>
你是一位资深小说编辑，擅长从文本中挖掘高价值的写作素材。
</角色>

<任务>
从给定的小说原文中摘录出精华片段，用于构建写作素材库。
</任务>

<原文>
{text}
</原文>

<摘录要求>
1. 每个片段 20-100 字，必须是原文摘录，不可改写
2. 只摘录有写作参考价值的精彩片段（优美的描写、传神的对话、深刻的心理刻画等）
3. 如果原文平淡无亮点，返回空列表即可
</摘录要求>

<输出字段>
返回 snippets 列表，每个 MaterialSnippet 包含：

1. essential_text (精华文本)
   - 从原文中摘录的片段，20-100字
   - 必须是原文，不可改写

2. category (描写技法) - 单选一个
   - 对话: 人物对白、独白
   - 动作: 动作描写、肢体语言
   - 心理: 内心活动、意识流
   - 环境: 场景、天气、氛围
   - 外貌: 人物外表、神态
   - 意象: 象征、比喻、特写

3. mood (情绪基调) - 单选一个
   - 喜悦 / 悲伤 / 愤怒 / 恐惧 / 温情 / 压抑 / 激昂 / 平静

4. tags (内容标签) - 多选，自由填写，标签应简洁有力，每个标签两个字，不超过3个标签
   - 场景类: 如 校园、都市、古风、雨夜、深夜...
   - 关系类: 如 爱情、友情、亲情、对手...
   - 情节类: 如 告别、重逢、冲突、成长、救赎...
   - 其他: 任何你认为有助于检索的关键词
</输出字段>
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
