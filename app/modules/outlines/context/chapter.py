from app.modules.base.context import BaseContext

from ..schemas.bible import Bible
from ..schemas.chapter import ChapterBlueprint, ChapterSceneBeat, ChapterSceneBlueprint
from ..schemas.substory import Substory, SubstoryActionNode


class ChapterBlueprintContext(BaseContext):
    bible: Bible
    substory: Substory
    cumulative_substory_summary: str
    pre_chapter_summary: str
    logic_nodes_to_process: list[SubstoryActionNode]


class ChapterBlueprintBrainstormContext(ChapterBlueprintContext):
    chapter_blueprint: ChapterBlueprint
    history: list[str]
    user_input: str


class ChapterSceneContext(ChapterBlueprintContext):
    last_scene_beat: ChapterSceneBeat | None
    chapter_blueprint: ChapterBlueprint
    scene_blueprint: ChapterSceneBlueprint


class ChapterContext(ChapterBlueprintContext):
    chapter_blueprint: ChapterBlueprint
