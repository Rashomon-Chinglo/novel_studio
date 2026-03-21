import functools

from langchain_openai import ChatOpenAI

from app.core.config import settings


@functools.lru_cache
def get_llm() -> ChatOpenAI:
    # ⚡ Bolt: Cache LLM initialization to prevent redundant creation of expensive ChatOpenAI clients
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,  # type: ignore[unknown-argument]
        base_url=settings.OPENAI_BASE_URL,  # type: ignore[unknown-argument]
        model=settings.OPENAI_MODEL,  # type: ignore[unknown-argument]
    )
