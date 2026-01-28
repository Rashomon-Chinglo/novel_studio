from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.core.llm import get_llm

from ..schemas.bible import Bible


def get_brainstorm_chain(prompt: ChatPromptTemplate):
    llm = get_llm(0.8)
    structured_llm = prompt | llm | StrOutputParser()
    return structured_llm


def get_bible_chain(prompt: ChatPromptTemplate):
    llm = get_llm(0.3)

    structured_llm = prompt | llm.with_structured_output(
        Bible, method="function_calling", strict=True
    )

    return structured_llm
