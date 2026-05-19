import functools

from langchain_openai import ChatOpenAI

from app.core.config import settings


@functools.cache
def get_llm() -> ChatOpenAI:
    # ⚡ Bolt Optimization: Cache the LLM instance to act as a singleton.
    # This minimizes memory footprint and initialization overhead since ChatOpenAI is thread-safe for stateless usage.
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,  # type: ignore[unknown-argument]
        base_url=settings.OPENAI_BASE_URL,  # type: ignore[unknown-argument]
        model=settings.OPENAI_MODEL,  # type: ignore[unknown-argument]
    )
