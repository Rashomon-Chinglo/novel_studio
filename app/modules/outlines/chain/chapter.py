from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.core.llm import get_llm

from ..schemas.chapter import ChapterBlueprint, ChapterScene


def get_chapter_blueprint_chain(prompt: ChatPromptTemplate):
    llm = get_llm(0.8)

    structured_llm = prompt | llm.with_structured_output(
        ChapterBlueprint, method="function_calling", strict=True
    )
    return structured_llm


def get_chapter_brainstorm_chain(prompt: ChatPromptTemplate):
    llm = get_llm(0.8)
    structured_llm = prompt | llm | StrOutputParser()
    return structured_llm


def get_chapter_scene_chain(prompt: ChatPromptTemplate):
    llm = get_llm(0.8)
    structured_llm = prompt | llm.with_structured_output(
        ChapterScene, method="function_calling", strict=True
    )
    return structured_llm
