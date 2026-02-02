import asyncio
import json
import uuid

from app.db.session import AsyncSessionLocal
from app.db.vector import get_vector_store
from app.models.snippet import Snippet
from app.modules.materials.context import MaterialsMiningContext
from app.modules.materials.engine import MaterialEngine
from app.modules.materials.schemas import ExtractedResult, MaterialSnippet


class MaterialService:
    def __init__(self):
        self.engine = MaterialEngine()
        self.vector_store = get_vector_store()

    async def mine(self, text: str) -> ExtractedResult:
        context = MaterialsMiningContext(text=text)
        return await self.engine.mine(context)

    async def process_content(self, title: str, full_text: str):
        segments = self.engine.split_text(full_text)
        semaphore = asyncio.Semaphore(2)

        async def worker(index, chunk_text):
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

    async def save_snippets(self, title: str, snippets: list[MaterialSnippet]):
        sql_snippets = []
        chroma_snippets = {
            "ids": [],
            "metadatas": [],
            "texts": [],
        }

        for snippet in snippets:
            snippet_id = str(uuid.uuid4())
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
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    session.add_all(sql_snippets)

            # Use async method to prevent blocking the event loop during vector store operations
            await self.vector_store.aadd_texts(**chroma_snippets)
        except Exception as e:
            print(f"Error saving snippets: {e}")
