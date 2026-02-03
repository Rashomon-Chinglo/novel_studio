from typing import ClassVar

from pydantic import BaseModel, Field

from app.modules.base.schemas import MaterialCategory, MaterialMood


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
