from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.core import get_llm


def get_chapter_summary_chain(prompt: ChatPromptTemplate):
    llm = get_llm()
    return prompt | llm | StrOutputParser()


def get_cumulative_substory_summary_chain(prompt: ChatPromptTemplate):
    llm = get_llm()
    return prompt | llm | StrOutputParser()
