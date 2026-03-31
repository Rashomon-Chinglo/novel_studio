import asyncio

from app.persistence import models as _models  # noqa: F401
from app.persistence.db.session import init_sqlite_db
from app.persistence.db.vector import get_vector_store


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
