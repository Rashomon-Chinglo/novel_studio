from pydantic import BaseModel, Field


class MaterialSnippet(BaseModel):
    essential_text: str = Field(description="从文章中摘录的精华文本，20-100字")
    category: str = Field(description="摘录文本的分类")
    tags: list[str] = Field(description="摘录文本的标签")
    mood: str = Field(description="摘录文本的情绪")


class ExtractedResult(BaseModel):
    snippets: list[MaterialSnippet] = Field(description="从文章中摘录的精华文本列表")
