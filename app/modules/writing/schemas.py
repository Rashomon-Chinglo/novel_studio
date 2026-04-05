from pydantic import BaseModel


class SceneChunk(BaseModel):
    content: str

    def prompt(self) -> str:
        if self.content.strip():
            return f"<上文内容>\n{self.content}\n</上文内容>"
        return "<上文内容>此为第一章，无前文，专注其它背景即可</上文内容>"


class WrittenChapter(BaseModel):
    chunks: list[SceneChunk]

    def prompt(self) -> str:
        content = "\n".join([chunk.content for chunk in self.chunks])
        return f"<章节正文>\n{content}\n</章节正文>"
