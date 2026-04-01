from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable

from app.core import get_llm

from ..schemas import Bible


def get_brainstorm_chain(prompt: ChatPromptTemplate) -> RunnableSerializable:
    llm = get_llm()
    structured_llm = prompt | llm | StrOutputParser()
    return structured_llm


def get_bible_chain(prompt: ChatPromptTemplate) -> RunnableSerializable:
    llm = get_llm()

    structured_llm = prompt | llm.with_structured_output(
        Bible, method="function_calling", strict=True
    )

    return structured_llm
