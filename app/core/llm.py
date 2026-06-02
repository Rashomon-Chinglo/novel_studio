import functools

from langchain_openai import ChatOpenAI

from app.core.config import settings


# ⚡ Bolt: Cache the LLM client singleton to avoid redundant initializations and memory overhead.
@functools.cache
def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,  # type: ignore[unknown-argument]
        base_url=settings.OPENAI_BASE_URL,  # type: ignore[unknown-argument]
        model=settings.OPENAI_MODEL,  # type: ignore[unknown-argument]
    )
