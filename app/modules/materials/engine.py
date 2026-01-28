import asyncio
import json
import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.db.session import AsyncSessionLocal
from app.db.vector import get_vector_store
from app.models.snippet import Snippet

from .chain import get_mining_chain
from .context import MaterialsMiningContext
from .prompt import MaterialsMiningPrompt
from .schemas import ExtractedResult, ExtractedSnippet


class MaterialEngine:
    def __init__(self):
        self.material_mining_prompt = MaterialsMiningPrompt()
        self.llm = get_mining_chain(self.material_mining_prompt.prompt)
        self.vector_store = get_vector_store()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=20,
            separators=["\n\n", "\n", "。", "！", "？"],
            length_function=len,
        )

    async def process_content(self, title: str, full_text: str):
        segments = self.splitter.split_text(full_text)
        semaphore = asyncio.Semaphore(2)

        async def worker(index, chunk_text):
            async with semaphore:
                try:
                    context = MaterialsMiningContext(text=chunk_text)
                    variables = self.material_mining_prompt.build_variables(context)
                    result: ExtractedResult = await self.llm.ainvoke(variables)
                    if not result.snippets:
                        return
                    await self.save_snippets(title, result.snippets)
                except Exception as e:
                    print(f"Error processing chunk {index}: {e}")
                    return index, None

        tasks = [worker(i, segment) for i, segment in enumerate(segments)]
        await asyncio.gather(*tasks)

    async def save_snippets(self, title: str, snippets: list[ExtractedSnippet]):
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
            print(f"Successfully saved snippet: {snippet.schema_json(indent=2)}")

        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    session.add_all(sql_snippets)

            self.vector_store.add_texts(**chroma_snippets)
        except Exception as e:
            print(f"Error saving snippets: {e}")
