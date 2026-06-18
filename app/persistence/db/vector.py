import functools

from langchain_chroma import Chroma
from langchain_community.embeddings import JinaEmbeddings

from app.core.config import settings


# Optimization: Cache Vector Store instance to prevent redundant instantiations
# Avoids reloading Chroma from disk on every call, significantly reducing I/O bottleneck
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
