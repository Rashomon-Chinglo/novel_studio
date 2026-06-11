import functools

from langchain_openai import ChatOpenAI

from app.core.config import settings


# ⚡ Bolt Optimization: Use @functools.cache to return a singleton instance of ChatOpenAI.
# This prevents repeated client initialization on every call, avoiding memory bloat
# and reducing unnecessary I/O overhead.
@functools.cache
def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,  # type: ignore[unknown-argument]
        base_url=settings.OPENAI_BASE_URL,  # type: ignore[unknown-argument]
        model=settings.OPENAI_MODEL,  # type: ignore[unknown-argument]
    )
