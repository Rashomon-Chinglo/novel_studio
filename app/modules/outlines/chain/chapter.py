from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable

from app.core.llm import get_llm

from ..schemas.chapter import ChapterBlueprint, ChapterScene


def get_chapter_blueprint_chain(prompt: ChatPromptTemplate) -> RunnableSerializable:
    llm = get_llm()

    structured_llm = prompt | llm.with_structured_output(
        ChapterBlueprint, method="function_calling", strict=True
    )
    return structured_llm


def get_chapter_brainstorm_chain(prompt: ChatPromptTemplate) -> RunnableSerializable:
    llm = get_llm()
    structured_llm = prompt | llm | StrOutputParser()
    return structured_llm


def get_chapter_scene_chain(prompt: ChatPromptTemplate) -> RunnableSerializable:
    llm = get_llm()
    structured_llm = prompt | llm.with_structured_output(
        ChapterScene, method="function_calling", strict=True
    )
    return structured_llm
