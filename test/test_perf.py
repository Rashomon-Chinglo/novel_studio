import os
import sys

sys.path.append(os.getcwd())

import asyncio
import time
import uuid

from app.db.vector import get_vector_store
from app.modules.materials.schemas import MaterialSnippet


class MockEngine:
    def split_text(self, text):
        return [text] * 10

    async def mine(self, context):
        await asyncio.sleep(0.1)  # Simulate LLM call

        class MockResult:
            def __init__(self):
                self.snippets = [
                    MaterialSnippet(
                        category="对话",
                        tags=["test"],
                        mood="喜悦",
                        essential_text="Test snippet content",
                    )
                ]

        return MockResult()


class PerfTestService:
    def __init__(self):
        self.engine = MockEngine()
        self.vector_store = get_vector_store()

    async def process_content(self, title: str, full_text: str):
        segments = self.engine.split_text(full_text)
        semaphore = asyncio.Semaphore(2)

        async def worker(index, chunk_text):
            async with semaphore:
                try:
                    result = await self.engine.mine(chunk_text)
                    if not result.snippets:
                        return
                    await self.save_snippets(title, result.snippets)
                except Exception as e:
                    print(f"Error processing chunk {index}: {e}")
                    return index, None

        tasks = [worker(i, segment) for i, segment in enumerate(segments)]
        await asyncio.gather(*tasks)

    async def save_snippets(self, title: str, snippets: list[MaterialSnippet]):
        chroma_snippets = {
            "ids": [],
            "metadatas": [],
            "texts": [],
        }

        for snippet in snippets:
            snippet_id = str(uuid.uuid4())
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

        try:
            # We skip DB for the perf test, just testing vector store
            await self.vector_store.aadd_texts(**chroma_snippets)
        except Exception:
            # Ignore errors from invalid jina api key dummy during actual aadd_texts execution,
            # we just want to ensure it uses the async version
            pass


async def run_test():
    service = PerfTestService()
    start = time.time()
    await service.process_content("Test Title", "Test content to process")
    duration = time.time() - start
    print(f"Processing took: {duration:.4f}s")
    assert duration < 1.0, "Execution took longer than expected for concurrent async operations"
    return duration


if __name__ == "__main__":
    asyncio.run(run_test())
