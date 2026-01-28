from langchain_openai import ChatOpenAI

from app.core.config import settings


def get_llm(temperature: float = 0.7) -> ChatOpenAI:
    return ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        model_name=settings.OPENAI_MODEL,
        temperature=temperature,
    )
