from pydantic import BaseModel

from app.modules.base import ChapterSummary, CumulativeSubstorySummary

from ..schemas import (
    Bible,
    ChapterBlueprint,
    ChapterOriginalSubstoryNodes,
    ChapterSceneBeat,
    ChapterSceneBlueprint,
    Substory,
)


class ChapterBlueprintContext(BaseModel):
    bible: Bible
    substory: Substory
    cumulative_substory_summary: CumulativeSubstorySummary
    pre_chapter_summary: ChapterSummary
    logic_nodes_to_process: ChapterOriginalSubstoryNodes


class ChapterSceneContext(ChapterBlueprintContext):
    last_scene_beat: ChapterSceneBeat | None
    chapter_blueprint: ChapterBlueprint
    scene_blueprint: ChapterSceneBlueprint


class ChapterContext(ChapterBlueprintContext):
    chapter_blueprint: ChapterBlueprint
