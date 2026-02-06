from pydantic import BaseModel

from app.modules.outlines.schemas.bible import Bible
from app.modules.outlines.schemas.chapter import Chapter as ChapterOutline
from app.modules.outlines.schemas.substory import Substory, SubstoryActionNode
from app.modules.writing.schemas import Chapter


class ChapterSummaryContext(BaseModel):
    bible: Bible
    substory: Substory
    original_logic_nodes: list[SubstoryActionNode]
    chapter_outline: ChapterOutline
    cumulative_substory_summary: str
    pre_chapter_summary: str
    chapter: Chapter


class SubstoryCumulativeSummaryContext(BaseModel):
    bible: Bible
    substory: Substory
    cumulative_substory_summary: str
    current_chapter_summary: str
