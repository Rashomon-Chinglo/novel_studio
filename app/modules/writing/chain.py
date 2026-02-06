from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.core.llm import get_llm


def get_scene_writing_chain(prompt: ChatPromptTemplate):
    llm = get_llm()
    structured_llm = prompt | llm | StrOutputParser()
    return structured_llm
