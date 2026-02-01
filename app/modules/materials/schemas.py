from typing import ClassVar, Literal

from pydantic import BaseModel, Field

# 描写技法 (单选，封闭式)
type MaterialCategory = Literal[
    "对话",  # 人物对白、独白
    "动作",  # 动作、肢体语言
    "心理",  # 内心活动、意识流
    "环境",  # 场景、天气、氛围
    "外貌",  # 人物外表、神态
    "意象",  # 象征、比喻、特写
]

# 情绪标签 (单选，封闭式)
type MaterialMood = Literal[
    "喜悦",  # 开心、幸福、温馨
    "悲伤",  # 难过、忧郁、失落
    "愤怒",  # 生气、不满
    "恐惧",  # 害怕、紧张、不安
    "温情",  # 感动、怀念、治愈
    "压抑",  # 沉重、绝望
    "激昂",  # 热血、振奋
    "平静",  # 淡然、释然
]


class MaterialSnippet(BaseModel):
    _prompt_labels: ClassVar[dict[str, str]] = {
        "essential_text": "精华文本",
        "category": "描写技法",
        "mood": "情绪",
        "tags": "内容标签",
    }

    essential_text: str = Field(description="从文章中摘录的精华文本，20-100字")
    category: MaterialCategory = Field(description="摘录文本的描写技法")
    mood: MaterialMood = Field(description="摘录文本的情绪基调")
    tags: list[str] = Field(description="摘录文本的内容标签，如场景、情节、主题等")

    def prompt(self, index: int | None = None) -> str:
        _index = f"{index}" if index else ""
        data = self.model_dump(exclude_none=True)
        bible = {self._prompt_labels.get(k, k): v for k, v in data.items()}

        content = "\n".join([f"- **{k}**: {v}" for k, v in bible.items()])
        return f"<参考素材{_index}>\n{content}\n</参考素材{_index}>"


class ExtractedResult(BaseModel):
    snippets: list[MaterialSnippet] = Field(description="从文章中摘录的精华文本列表")
