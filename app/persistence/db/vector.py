import functools

from langchain_chroma import Chroma
from langchain_community.embeddings import JinaEmbeddings

from app.core.config import settings


# ⚡ Bolt: Cache expensive Vector Store client creation to avoid redundant initialization
# This prevents creating a new Chroma and JinaEmbeddings instance on every get_vector_store() call,
# reducing memory usage and initialization overhead, and ensures singleton behavior for the DB connection.
@functools.cache
def get_vector_store():
    embeddings = JinaEmbeddings(  # type: ignore[missing-argument]
        jina_api_key=settings.JINA_API_KEY,  # type: ignore[invalid-argument-type]
        jina_url=settings.JINA_API_URL,  # type: ignore[invalid-argument-type]
        model_name="jina-embeddings-v3",
    )
    return Chroma(
        collection_name=settings.CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=settings.CHROMA_URL,
    )
