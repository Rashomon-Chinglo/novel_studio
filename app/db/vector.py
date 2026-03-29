import functools

from langchain_chroma import Chroma
from langchain_community.embeddings import JinaEmbeddings

from app.core.config import settings

# def get_chroma_collection():
#     client = chromadb.PersistentClient(path=settings.CHROMA_URL)

#     collection = client.get_or_create_collection(name=settings.CHROMA_COLLECTION_NAME)
#     return collection


@functools.lru_cache
def get_vector_store():
    """
    ⚡ Bolt Optimization:
    Uses lru_cache to ensure the vector store and embeddings client are initialized
    only once. This prevents redundant, expensive instantiations across the app.
    """
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
