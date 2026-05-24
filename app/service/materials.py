import asyncio
import json
from collections.abc import Callable

from app.core import new_id
from app.modules.materials import (
    ExtractedResult,
    MaterialEngine,
    MaterialsMiningContext,
    MaterialSnippet,
)
from app.persistence import SqlAlchemyUnitOfWork, get_vector_store
from app.persistence.models import Snippet


class MaterialService:
    def __init__(
        self,
        engine: MaterialEngine | None = None,
        vector_store=None,
        uow_factory: Callable[[], SqlAlchemyUnitOfWork] = SqlAlchemyUnitOfWork,
    ) -> None:
        self.engine = engine or MaterialEngine()
        self.vector_store = vector_store or get_vector_store()
        self.uow_factory = uow_factory

    async def mine(self, text: str) -> ExtractedResult:
        context = MaterialsMiningContext(text=text)
        return await self.engine.mine(context)

    async def process_content(self, title: str, full_text: str):
        segments = self.engine.split_text(full_text)
        semaphore = asyncio.Semaphore(2)

        async def worker(index: int, chunk_text: str):
            async with semaphore:
                try:
                    result: ExtractedResult = await self.mine(chunk_text)
                    if not result.snippets:
                        return
                    await self.save_snippets(title, result.snippets)
                except Exception as e:
                    print(f"Error processing chunk {index}: {e}")
                    return index, None

        tasks = [worker(i, segment) for i, segment in enumerate(segments)]
        await asyncio.gather(*tasks)

    async def save_snippets(self, title: str, snippets: list[MaterialSnippet]) -> None:
        sql_snippets = []
        chroma_snippets = {
            "ids": [],
            "metadatas": [],
            "texts": [],
        }

        for snippet in snippets:
            snippet_id = new_id()
            sql_snippets.append(
                Snippet(
                    id=snippet_id,
                    title=title,
                    category=snippet.category,
                    tags=json.dumps(snippet.tags, ensure_ascii=False),
                    mood=snippet.mood,
                    content=snippet.essential_text,
                )
            )
            chroma_snippets["ids"].append(snippet_id)
            chroma_snippets["metadatas"].append(
                {
                    "title": title,
                    "category": snippet.category,
                    "tags": ",".join(snippet.tags),
                    "mood": snippet.mood,
                    "content": snippet.essential_text,
                }
            )
            chroma_snippets["texts"].append(
                f"""
            类型：{snippet.category}，标签：{",".join(snippet.tags)}，情绪：{snippet.mood}，内容：{snippet.essential_text}
            """
            )
            print(f"Successfully saved snippet: {snippet.model_dump_json(indent=2)}")

        try:
            async with self.uow_factory() as uow:
                uow.materials.snippets.add_many(sql_snippets)
                await uow.commit()

            # ⚡ Bolt: Use aadd_texts instead of add_texts to prevent blocking the async event loop
            await self.vector_store.aadd_texts(**chroma_snippets)
        except Exception as e:
            print(f"Error saving snippets: {e}")
