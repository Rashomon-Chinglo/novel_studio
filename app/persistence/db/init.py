from app.persistence.db.schema import init_db_schema
from app.persistence.db.vector import get_vector_store


async def initialize_persistence(*, initialize_vector_store: bool = True) -> None:
    await init_db_schema()

    if initialize_vector_store:
        get_vector_store()
