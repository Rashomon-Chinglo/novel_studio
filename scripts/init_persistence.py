import asyncio

from app.persistence import initialize_persistence


async def init_persistence() -> None:
    print("🚀 Initializing persistence...")

    try:
        await initialize_persistence()
    except Exception as e:
        print(f"❌ Failed to initialize persistence: {e}")
        return

    print("✅ Persistence initialized successfully")


if __name__ == "__main__":
    asyncio.run(init_persistence())
