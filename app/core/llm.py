import functools

from langchain_openai import ChatOpenAI

from app.core.config import settings


# Optimization: Use @functools.cache to ensure ChatOpenAI client is a singleton.
# Why: Redundant client instantiation increases memory footprint and initialization overhead.
# Impact: Reduces memory usage and speeds up repeated LLM initializations.
@functools.cache
def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,  # type: ignore[unknown-argument]
        base_url=settings.OPENAI_BASE_URL,  # type: ignore[unknown-argument]
        model=settings.OPENAI_MODEL,  # type: ignore[unknown-argument]
    )
