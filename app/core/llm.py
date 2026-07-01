import functools

from langchain_openai import ChatOpenAI

from app.core.config import settings


@functools.cache
def get_llm() -> ChatOpenAI:
    # ⚡ Bolt Optimization: Cache the ChatOpenAI client instance.
    # Why: get_llm() is called frequently across chains and modules. Repeated instantiation
    #      causes unnecessary I/O and memory bloat.
    # Impact: Reuses a singleton client, reducing memory footprint and initialization overhead.
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,  # type: ignore[unknown-argument]
        base_url=settings.OPENAI_BASE_URL,  # type: ignore[unknown-argument]
        model=settings.OPENAI_MODEL,  # type: ignore[unknown-argument]
    )
