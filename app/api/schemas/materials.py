"""Materials API schemas."""

from pydantic import BaseModel, Field

from app.modules.base import MaterialCategory, MaterialMood
from app.modules.materials import MaterialSnippet


class MineMaterialsRequest(BaseModel):
    full_text: str


class MineMaterialsResponse(BaseModel):
    created_snippet_count: int


class SemanticSearchMaterialsRequest(BaseModel):
    query: str
    limit: int = 8
    category: MaterialCategory | None = None
    mood: MaterialMood | None = None


class LexicalSearchMaterialsRequest(BaseModel):
    query: str | None = None
    limit: int = 8
    category: MaterialCategory | None = None
    mood: MaterialMood | None = None
    tags: list[str] | None = None


class MaterialsSearchResponse(BaseModel):
    snippets: list[MaterialSnippet] = Field(default_factory=list)
