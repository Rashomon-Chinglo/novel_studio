# test_sqlite.py
import asyncio
import json
import os
import sys

from sqlalchemy import func, select

# 路径修补
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import AsyncSessionLocal
from app.models.snippet import Snippet


async def check_sqlite():
    print("🔍 [SQLite 验尸官] 正在检查关系型数据库...")

    async with AsyncSessionLocal() as session:
        # 1. 检查连接 & 统计总数
        try:
            # 使用 func.count 统计行数
            result = await session.execute(select(func.count(Snippet.id)))
            count = result.scalar()
            print(f"   📊 表中记录总数: {count}")

            if count == 0:
                print("   ⚠️  表是空的！")
                return
        except Exception as e:
            print(f"   ❌ 连接或查询失败: {e}")
            print("   💡 提示: 可能是表没建？请运行 python init_db.py")
            return

        # 2. 详细检查最近入库的 3 条
        print("\n   👀 [最新 3 条数据预览]")

        # 按 id 倒序或者随机取都行，这里简单起见直接取 limit
        stmt = select(Snippet).limit(3)
        result = await session.execute(stmt)
        snippets = result.scalars().all()

        for i, item in enumerate(snippets):
            print(f"\n   --- Record {i + 1} ---")
            print(f"   🆔 ID       : {item.id}")
            print(f"   📖 书名     : {item.title}")
            print(f"   🗂️  分类     : {item.category}")
            print(f"   🎭 情绪     : {item.mood}")

            # 3. 重点检查 JSON 字段解析
            # 在 SQLite 里 tags 是存成字符串 '["a", "b"]' 的
            # 我们要验证取出来后能不能当列表用
            try:
                tags_data = json.loads(item.tags)  # type: ignore[arg-type]
                if isinstance(tags_data, list):
                    print(f"   ✅ 标签(List): {tags_data}")
                else:
                    print(f"   ⚠️  标签解析后不是 List: {type(tags_data)}")
            except Exception:
                print(f"   ❌ 标签 JSON 解析失败 (存进去的不是合法 JSON?): {item.tags}")

            # 内容预览 (处理换行符)
            content_preview = item.content.replace("\n", " ")
            print(f"   📝 内容     : {content_preview}")

    print("\n✅ SQLite 检查完毕。")


if __name__ == "__main__":
    asyncio.run(check_sqlite())
