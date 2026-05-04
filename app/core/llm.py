import functools

from langchain_openai import ChatOpenAI

from app.core.config import settings


@functools.cache
def get_llm() -> ChatOpenAI:
    # ⚡ Bolt Optimization: Cache the LLM instance to prevent redundant initialization of the ChatOpenAI client
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,  # type: ignore[unknown-argument]
        base_url=settings.OPENAI_BASE_URL,  # type: ignore[unknown-argument]
        model=settings.OPENAI_MODEL,  # type: ignore[unknown-argument]
    )
