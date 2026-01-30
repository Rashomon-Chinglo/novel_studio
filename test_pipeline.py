import asyncio
import os
import sys
from pathlib import Path

import aiofiles
from sqlalchemy import func, select

# Ensure app package is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import AsyncSessionLocal
from app.db.vector import get_vector_store
from app.models.snippet import Snippet
from app.service.materials import MaterialService


async def get_content():
    path = Path("/home/rashomon/projects/novel_studio/test")
    files = [
        "0003_第3章 睡觉！.txt",
        "0010_第10章 冰箱.txt",
    ]
    for file in files:
        file_path = path / file
        if not file_path.exists():
            print(f"⚠️ Warning: File not found: {file_path}")
            continue
        async with aiofiles.open(file_path, encoding="utf-8") as f:
            content = await f.read()
            yield file, content


async def verify_results():
    print("\n🔍 [Verification] Checking results...")

    # Check SQLite
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(func.count(Snippet.id)))
        sql_count = result.scalar()
        print(f"   📊 SQLite - Total Snippets: {sql_count}")

    # Check Chroma
    try:
        vector_store = get_vector_store()
        chroma_ids = vector_store.get()["ids"]
        print(f"   📊 Chroma - Total IDs: {len(chroma_ids)}")
    except Exception as e:
        print(f"   ❌ Chroma check failed: {e}")


async def main():
    service = MaterialService()

    print("🚀 Starting Materials Processing Pipeline (Single Item Test)...")
    async for title, content in get_content():
        print(f"📝 Processing: {title}...")
        await service.process_content(title, content)
        break  # Only test one file to save tokens

    await verify_results()
    print("\n✨ Pipeline test completed.")


if __name__ == "__main__":
    asyncio.run(main())
