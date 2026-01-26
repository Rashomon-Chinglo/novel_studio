from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.llm import get_llm
from ..schemas.substory import Substory


def get_brainstorm_chain(prompt: ChatPromptTemplate):
    llm = get_llm(0.8)
    structured_llm = prompt | llm | StrOutputParser()
    return structured_llm


def get_substory_chain(prompt: ChatPromptTemplate):
    llm = get_llm(0.3)
    structured_llm = prompt | llm.with_structured_output(
        Substory, method="function_calling", strict=True
    )
    return structured_llm
