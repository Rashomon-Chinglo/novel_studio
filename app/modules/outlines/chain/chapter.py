from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.core.llm import get_llm

from ..schemas.bible import Bible
from ..schemas.chapter import ChapterBlueprint
from ..schemas.substory import Substory

BLUEPRINT_INIT_PROMPT = """
{overview_outline}
{substory_outline}
{substory_summary}
{before_chapter_summary}
{format_instructions}
"""


def get_blueprint_init_chain(bible: Bible, substory: Substory):
    llm = get_llm(0.8)
    parser = JsonOutputParser(pydantic_object=ChapterBlueprint)
    prompt = ChatPromptTemplate.from_messages(
        [("system", BLUEPRINT_INIT_PROMPT)]
    ).partial(
        overview_outline=bible.model_dump_json(
            include=[
                "worldview_tone",
                "main_conflict",
                "ending_vision",
                "key_roles_summary",
            ]
        ),
        substory=substory.model_dump_json(
            include=[
                "core_conflict",
                "status_change",
                "logic_nodes",
            ]
        ),
    )
    structured_llm = prompt | llm | parser | (lambda x: ChapterBlueprint(**x))
    return structured_llm


BRAINSTORM_PROMPT = """
"""
