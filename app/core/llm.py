import functools

from langchain_openai import ChatOpenAI

from app.core.config import settings


# 💡 What: Add @functools.cache to memoize the LLM client instance
# 🎯 Why: ChatOpenAI is thread-safe and stateless for our usage. Re-initializing it for every call causes unnecessary I/O and object creation overhead.
# 📊 Impact: Eliminates redundant client initialization overhead across the application, saving memory and CPU cycles per request.
@functools.cache
def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,  # type: ignore[unknown-argument]
        base_url=settings.OPENAI_BASE_URL,  # type: ignore[unknown-argument]
        model=settings.OPENAI_MODEL,  # type: ignore[unknown-argument]
    )
