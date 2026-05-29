import functools

from langchain_openai import ChatOpenAI

from app.core.config import settings


@functools.cache
def get_llm() -> ChatOpenAI:
    # ⚡ Bolt: Cache the ChatOpenAI client as a singleton to avoid repeated initialization overhead.
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,  # type: ignore[unknown-argument]
        base_url=settings.OPENAI_BASE_URL,  # type: ignore[unknown-argument]
        model=settings.OPENAI_MODEL,  # type: ignore[unknown-argument]
    )
