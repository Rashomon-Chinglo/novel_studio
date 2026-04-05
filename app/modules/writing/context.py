from pydantic import BaseModel

from app.modules.base import ChapterSummary, CumulativeSubstorySummary
from app.modules.materials import MaterialSnippet
from app.modules.outlines.schemas import (
    Bible,
    ChapterBlueprint,
    ChapterOriginalSubstoryNodes,
    ChapterOutline,
    ChapterScene,
    ChapterSceneBlueprint,
    Substory,
)
from app.modules.writing.schemas import SceneChunk


class ChapterSceneWritingContext(BaseModel):
    bible: Bible
    substory: Substory
    original_logic_nodes: ChapterOriginalSubstoryNodes
    chapter_blueprint: ChapterBlueprint
    scene_blueprint: ChapterSceneBlueprint
    scene: ChapterScene
    cumulative_substory_summary: CumulativeSubstorySummary
    pre_chapter_summary: ChapterSummary
    previous_scene_chunk: SceneChunk
    materials: list[MaterialSnippet]


class ChapterWritingContext(BaseModel):
    bible: Bible
    substory: Substory
    original_logic_nodes: ChapterOriginalSubstoryNodes
    chapter_blueprint: ChapterBlueprint
    chapter_outline: ChapterOutline
    cumulative_substory_summary: CumulativeSubstorySummary
    pre_chapter_summary: ChapterSummary
    previous_scene_chunk: SceneChunk
