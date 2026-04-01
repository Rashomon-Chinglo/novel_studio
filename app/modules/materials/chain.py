from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable

from app.core import get_llm

from .schemas import ExtractedResult


def get_mining_chain(prompt: ChatPromptTemplate) -> RunnableSerializable:
    llm = get_llm()
    structured_llm = prompt | llm.with_structured_output(
        ExtractedResult, method="function_calling", strict=True
    )

    return structured_llm
