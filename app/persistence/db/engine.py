from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


def _engine_connect_args(database_url: str) -> dict[str, object]:
    if database_url.startswith("sqlite+aiosqlite://"):
        return {"check_same_thread": False}
    return {}


def create_db_engine():
    return create_async_engine(
        settings.sqlalchemy_database_url,
        echo=False,
        connect_args=_engine_connect_args(settings.sqlalchemy_database_url),
    )


def create_session_factory(database_engine):
    return async_sessionmaker(
        bind=database_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


engine = create_db_engine()
SessionFactory = create_session_factory(engine)
