import asyncio

from app.persistence import get_vector_store, init_sqlite_db


async def init_db():
    print("🚀 Initializing database...")

    try:
        await init_sqlite_db()
    except Exception as e:
        print(f"❌ Failed to initialize SQLite database: {e}")
        return

    try:
        get_vector_store()
    except Exception as e:
        print(f"❌ Failed to initialize ChromaDB collection: {e}")
        return

    print("✅ Database initialized successfully")


if __name__ == "__main__":
    # 启动事件循环
    asyncio.run(init_db())
