from pydantic import BaseModel

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.materials.schemas import MaterialSnippet
from app.modules.outlines.schemas.bible import Bible
from app.modules.outlines.schemas.chapter import (
    ChapterBlueprint,
    ChapterOutline,
    ChapterScene,
    ChapterSceneBlueprint,
)
from app.modules.outlines.schemas.substory import ChapterOriginalSubstoryNodes, Substory


class ChapterSceneWritingContext(BaseModel):
    bible: Bible
    substory: Substory
    original_logic_nodes: ChapterOriginalSubstoryNodes
    chapter_blueprint: ChapterBlueprint
    scene_blueprint: ChapterSceneBlueprint
    scene: ChapterScene
    cumulative_substory_summary: CumulativeSubstorySummary
    pre_chapter_summary: ChapterSummary
    previous_content: str
    materials: list[MaterialSnippet]


class ChapterWritingContext(BaseModel):
    bible: Bible
    substory: Substory
    original_logic_nodes: ChapterOriginalSubstoryNodes
    chapter_blueprint: ChapterBlueprint
    chapter_outline: ChapterOutline
    cumulative_substory_summary: CumulativeSubstorySummary
    pre_chapter_summary: ChapterSummary
    previous_content: str
