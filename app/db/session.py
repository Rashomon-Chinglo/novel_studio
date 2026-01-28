from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings

engine = create_async_engine(
    settings.SQLITE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def init_sqlite_db():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(f"✅ Initialized SQLite database at {settings.SQLITE_URL}")
