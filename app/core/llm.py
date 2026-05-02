import functools

from langchain_openai import ChatOpenAI

from app.core.config import settings


# ⚡ Bolt: Cache expensive LLM client creation to avoid redundant initialization
# This prevents creating a new ChatOpenAI instance on every get_llm() call,
# reducing memory usage and initialization overhead.
@functools.cache
def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,  # type: ignore[unknown-argument]
        base_url=settings.OPENAI_BASE_URL,  # type: ignore[unknown-argument]
        model=settings.OPENAI_MODEL,  # type: ignore[unknown-argument]
    )
