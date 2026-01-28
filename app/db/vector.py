from langchain_chroma import Chroma
from langchain_community.embeddings import JinaEmbeddings

from app.core.config import settings

# def get_chroma_collection():
#     client = chromadb.PersistentClient(path=settings.CHROMA_URL)

#     collection = client.get_or_create_collection(name=settings.CHROMA_COLLECTION_NAME)
#     return collection


def get_vector_store():
    embeddings = JinaEmbeddings(
        jina_api_key=settings.JINA_API_KEY,
        jina_url=settings.JINA_URL,
        model_name="jina-embeddings-v3",
    )
    return Chroma(
        collection_name=settings.CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=settings.CHROMA_URL,
    )
