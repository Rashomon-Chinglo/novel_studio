import functools

from langchain_openai import ChatOpenAI

from app.core.config import settings


@functools.lru_cache
def get_llm() -> ChatOpenAI:
    # ⚡ Bolt: Cache the LLM client to prevent redundant initializations
    # and connection pool creations on every request.
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,  # type: ignore[unknown-argument]
        base_url=settings.OPENAI_BASE_URL,  # type: ignore[unknown-argument]
        model=settings.OPENAI_MODEL,  # type: ignore[unknown-argument]
    )
