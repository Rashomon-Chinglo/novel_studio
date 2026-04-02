from app.core.config import settings
from app.persistence.db.base import Base
from app.persistence.db.engine import engine


async def init_db_schema() -> None:
    from app.persistence.models import register_models

    register_models()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(f"✅ Initialized database schema at {settings.sqlalchemy_database_url}")
