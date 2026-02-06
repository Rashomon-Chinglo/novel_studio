from pydantic import BaseModel


class SceneChunk(BaseModel):
    content: str


class Chapter(BaseModel):
    chunks: list[SceneChunk]
