import asyncio
import json
from collections.abc import Callable
from typing import cast

from app.modules.base import MaterialCategory, MaterialMood
from app.modules.materials import (
    ExtractedResult,
    MaterialEngine,
    MaterialsMiningContext,
    MaterialSnippet,
)
from app.persistence import SqlAlchemyUnitOfWork
from app.persistence.indexes import ChromaSnippetIndex, SnippetIndex
from app.persistence.models import Snippet


class MaterialService:
    def __init__(
        self,
        engine: MaterialEngine | None = None,
        snippet_index: SnippetIndex | None = None,
        uow_factory: Callable[[], SqlAlchemyUnitOfWork] = SqlAlchemyUnitOfWork,
    ) -> None:
        self.engine = engine or MaterialEngine()
        self.snippet_index = snippet_index or ChromaSnippetIndex()
        self.uow_factory = uow_factory

    async def create_snippets(self, material_snippets: list[MaterialSnippet]) -> list[str]:
        snippets: list[Snippet] = []
        for material_snippet in material_snippets:
            snippets.append(
                Snippet(
                    category=material_snippet.category,
                    tags=json.dumps(material_snippet.tags, ensure_ascii=False),
                    mood=material_snippet.mood,
                    content=material_snippet.essential_text,
                )
            )
        async with self.uow_factory() as uow:
            uow.materials.snippets.add_many(snippets)
            await uow.commit()
        await self.snippet_index.save_snippets(snippets)
        return [snippet.id for snippet in snippets]

    async def mine_content(self, full_text: str) -> int:
        segments = self.engine.split_text(full_text)
        semaphore = asyncio.Semaphore(2)

        async def worker(index: int, chunk_text: str) -> int:
            async with semaphore:
                try:
                    context = MaterialsMiningContext(text=chunk_text)
                    result: ExtractedResult = await self.engine.mine(context)
                except Exception as exc:
                    raise RuntimeError(f"Failed to mine chunk {index}.") from exc

                if not result.snippets:
                    return 0

                try:
                    created_ids = await self.create_snippets(result.snippets)
                except Exception as exc:
                    raise RuntimeError(f"Failed to persist chunk {index}.") from exc

                return len(created_ids)

        tasks = [worker(i, segment) for i, segment in enumerate(segments)]
        results = await asyncio.gather(*tasks)
        return sum(results)

    def _to_schema(self, snippet: Snippet) -> MaterialSnippet:
        return MaterialSnippet(
            essential_text=snippet.content,
            category=cast(MaterialCategory, snippet.category),
            mood=cast(MaterialMood, snippet.mood),
            tags=json.loads(snippet.tags),
        )

    async def search_semantic(
        self,
        *,
        query: str,
        limit: int = 8,
        category: MaterialCategory | None = None,
        mood: MaterialMood | None = None,
    ) -> list[MaterialSnippet]:
        normalized_query = query.strip()
        if not normalized_query:
            return []

        return await self.snippet_index.search_snippets(
            query=normalized_query,
            limit=limit,
            category=category,
            mood=mood,
        )

    async def search_lexical(
        self,
        *,
        query: str | None = None,
        limit: int = 8,
        category: MaterialCategory | None = None,
        mood: MaterialMood | None = None,
        tags: list[str] | None = None,
    ) -> list[MaterialSnippet]:
        async with self.uow_factory() as uow:
            snippets = await uow.materials.snippets.search(
                query=query.strip() if query else None,
                limit=limit,
                category=category,
                mood=mood,
                tags=tags,
            )

        return [self._to_schema(snippet) for snippet in snippets]
