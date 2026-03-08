from pydantic import BaseModel

from app.modules.outlines.schemas.bible import Bible
from app.modules.outlines.schemas.chapter import Chapter as ChapterOutline
from app.modules.outlines.schemas.substory import ChapterOriginalSubstoryNodes, Substory
from app.modules.writing.schemas import Chapter

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary


class ChapterSummaryContext(BaseModel):
    bible: Bible
    substory: Substory
    original_logic_nodes: ChapterOriginalSubstoryNodes
    chapter_outline: ChapterOutline
    cumulative_substory_summary: CumulativeSubstorySummary
    pre_chapter_summary: ChapterSummary
    chapter: Chapter


class SubstoryCumulativeSummaryContext(BaseModel):
    bible: Bible
    substory: Substory
    cumulative_substory_summary: CumulativeSubstorySummary
    current_chapter_summary: ChapterSummary
