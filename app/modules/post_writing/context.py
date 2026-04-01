from pydantic import BaseModel

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.outlines.schemas.bible import Bible
from app.modules.outlines.schemas.chapter import ChapterOutline
from app.modules.outlines.schemas.substory import ChapterOriginalSubstoryNodes, Substory
from app.modules.writing.schemas import WrittenChapter


class ChapterSummaryContext(BaseModel):
    bible: Bible
    substory: Substory
    original_logic_nodes: ChapterOriginalSubstoryNodes
    chapter_outline: ChapterOutline
    cumulative_substory_summary: CumulativeSubstorySummary
    pre_chapter_summary: ChapterSummary
    written_chapter: WrittenChapter


class SubstoryCumulativeSummaryContext(BaseModel):
    bible: Bible
    substory: Substory
    cumulative_substory_summary: CumulativeSubstorySummary
    current_chapter_summary: ChapterSummary
