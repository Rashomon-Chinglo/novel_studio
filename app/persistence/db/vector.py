import functools

from langchain_chroma import Chroma
from langchain_community.embeddings import JinaEmbeddings

from app.core.config import settings


@functools.cache
def get_vector_store():
    # ⚡ Bolt: Cache the initialization of the expensive Vector Store client to improve performance
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
