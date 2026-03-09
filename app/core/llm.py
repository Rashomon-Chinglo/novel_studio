import functools

from langchain_openai import ChatOpenAI

from app.core.config import settings


# Cache expensive ChatOpenAI client initialization to ensure it acts as a singleton.
# This avoids a significant performance bottleneck when the function is called repeatedly.
@functools.lru_cache
def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,  # type: ignore[unknown-argument]
        base_url=settings.OPENAI_BASE_URL,  # type: ignore[unknown-argument]
        model=settings.OPENAI_MODEL,  # type: ignore[unknown-argument]
    )
