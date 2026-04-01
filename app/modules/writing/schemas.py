from pydantic import BaseModel


class SceneChunk(BaseModel):
    content: str

    def prompt(self) -> str:
        return self.content


class WrittenChapter(BaseModel):
    chunks: list[SceneChunk]

    def prompt(self) -> str:
        content = "\n".join([chunk.prompt() for chunk in self.chunks])
        return f"<章节正文>\n{content}\n</章节正文>"
