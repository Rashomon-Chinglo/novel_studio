import json
from collections.abc import Sequence
from typing import Protocol

from langchain_chroma import Chroma

from app.modules.base import MaterialCategory, MaterialMood
from app.modules.materials import MaterialSnippet
from app.persistence import get_vector_store
from app.persistence.models import Snippet


class SnippetIndex(Protocol):
    async def save_snippets(self, snippets: Sequence[Snippet]) -> None: ...

    async def search_snippets(
        self,
        *,
        query: str,
        limit: int = 8,
        category: MaterialCategory | None = None,
        mood: MaterialMood | None = None,
    ) -> list[MaterialSnippet]: ...


class ChromaSnippetIndex(SnippetIndex):
    def __init__(self, vector_store: Chroma | None = None) -> None:
        self.vector_store = vector_store or get_vector_store()

    def _loads_tags(self, tags: str) -> list[str]:
        return json.loads(tags)

    def _build_filter(
        self,
        *,
        category: MaterialCategory | None,
        mood: MaterialMood | None,
    ) -> dict[str, str] | None:
        metadata_filter: dict[str, str] = {}
        if category is not None:
            metadata_filter["category"] = category
        if mood is not None:
            metadata_filter["mood"] = mood
        return metadata_filter or None

    async def save_snippets(self, snippets: Sequence[Snippet]) -> None:
        ids: list[str] = []
        metadatas: list[dict[str, str]] = []
        texts: list[str] = []
        for snippet in snippets:
            tags = self._loads_tags(snippet.tags)
            ids.append(snippet.id)
            metadatas.append(
                {
                    "category": snippet.category,
                    "tags": snippet.tags,
                    "mood": snippet.mood,
                    "content": snippet.content,
                }
            )
            texts.append(
                f"类型：{snippet.category}，"
                f"标签：{','.join(tags)}，"
                f"情绪：{snippet.mood}，"
                f"内容：{snippet.content}"
            )
        self.vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)

    async def search_snippets(
        self,
        *,
        query: str,
        limit: int = 8,
        category: MaterialCategory | None = None,
        mood: MaterialMood | None = None,
    ) -> list[MaterialSnippet]:
        results = self.vector_store.similarity_search(
            query,
            k=limit,
            filter=self._build_filter(category=category, mood=mood),
        )
        return [
            MaterialSnippet(
                essential_text=result.metadata["content"],
                category=result.metadata["category"],
                mood=result.metadata["mood"],
                tags=self._loads_tags(result.metadata["tags"]),
            )
            for result in results
        ]
