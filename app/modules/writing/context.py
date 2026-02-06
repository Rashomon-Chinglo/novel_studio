from pydantic import BaseModel

from app.modules.materials.schemas import MaterialSnippet
from app.modules.outlines.schemas.bible import Bible
from app.modules.outlines.schemas.chapter import (
    Chapter,
    ChapterBlueprint,
    ChapterScene,
    ChapterSceneBlueprint,
)
from app.modules.outlines.schemas.substory import Substory, SubstoryActionNode


class ChapterSceneWritingContext(BaseModel):
    bible: Bible
    substory: Substory
    original_logic_nodes: list[SubstoryActionNode]
    chapter_blueprint: ChapterBlueprint
    scene_blueprint: ChapterSceneBlueprint
    scene: ChapterScene
    cumulative_substory_summary: str
    pre_chapter_summary: str
    previous_content: str
    materials: list[MaterialSnippet]


class ChapterWritingContext(BaseModel):
    bible: Bible
    substory: Substory
    original_logic_nodes: list[SubstoryActionNode]
    chapter_blueprint: ChapterBlueprint
    chapter: Chapter
    cumulative_substory_summary: str
    pre_chapter_summary: str
    previous_content: str
