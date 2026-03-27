import functools

from langchain_openai import ChatOpenAI

from app.core.config import settings


# ⚡ Bolt: Cache LLM instantiation to avoid redundant network/memory overhead.
# Expected Impact: Eliminates recurring ChatOpenAI setup time (~10-50ms) per call.
@functools.lru_cache(maxsize=1)
def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,  # type: ignore[unknown-argument]
        base_url=settings.OPENAI_BASE_URL,  # type: ignore[unknown-argument]
        model=settings.OPENAI_MODEL,  # type: ignore[unknown-argument]
    )
