from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable

from app.core import get_llm

from ..schemas import ChapterBlueprint, ChapterScene


def get_chapter_blueprint_chain(prompt: ChatPromptTemplate) -> RunnableSerializable:
    llm = get_llm()

    structured_llm = prompt | llm.with_structured_output(
        ChapterBlueprint, method="function_calling", strict=True
    )
    return structured_llm
def get_chapter_scene_chain(prompt: ChatPromptTemplate) -> RunnableSerializable:
    llm = get_llm()
    structured_llm = prompt | llm.with_structured_output(
        ChapterScene, method="function_calling", strict=True
    )
    return structured_llm
