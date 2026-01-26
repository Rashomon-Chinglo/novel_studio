import asyncio
import aiofiles
from pathlib import Path
from app.modules.materials.engine import MaterialEngine


async def get_content():
    path = Path("/home/rashomon/projects/novel_studio/test")
    files = [
        "0003_第3章 睡觉！.txt",
        "0010_第10章 冰箱.txt",
        # "0012_第12章 楼道里的人.txt",
    ]
    for file in files:
        async with aiofiles.open(path / file, "r", encoding="utf-8") as f:
            content = await f.read()
            yield file, content


async def main():
    material_engine = MaterialEngine()
    async for title, content in get_content():
        await material_engine.process_content(title, content)


if __name__ == "__main__":
    asyncio.run(main())
