from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable

from app.core.llm import get_llm

from ..schemas.substory import Substory


def get_brainstorm_chain(prompt: ChatPromptTemplate) -> RunnableSerializable:
    llm = get_llm()
    structured_llm = prompt | llm | StrOutputParser()
    return structured_llm


def get_substory_chain(prompt: ChatPromptTemplate) -> RunnableSerializable:
    llm = get_llm()
    structured_llm = prompt | llm.with_structured_output(
        Substory, method="function_calling", strict=True
    )
    return structured_llm
