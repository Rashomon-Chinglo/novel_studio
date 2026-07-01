import functools

from langchain_chroma import Chroma
from langchain_community.embeddings import JinaEmbeddings

from app.core.config import settings


@functools.cache
def get_vector_store():
    # ⚡ Bolt Optimization: Cache the VectorStore client instance.
    # Why: get_vector_store() instantiates Chroma and JinaEmbeddings. Doing this repeatedly
    #      is expensive, creates unnecessary I/O, and increases memory footprint.
    # Impact: Yields a singleton vector store across the application, significantly improving performance.
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
