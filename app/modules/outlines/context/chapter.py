from app.modules.base.context import BaseContext
from ..schemas.bible import Bible
from ..schemas.substory import Substory
from ..schemas.substory import SubstoryActionNode
from ..schemas.chapter import ChapterBlueprint
from ..schemas.chapter import SceneBlueprint
from ..schemas.chapter import SceneBeat


class ChapterBlueprintContext(BaseContext):
    bible: Bible
    substory: Substory
    cumulative_substory_summary: str
    pre_chapter_summary: str
    logic_nodes_to_process: list[SubstoryActionNode]

    def format_logic_nodes_to_process(self) -> str:
        return "\n".join(
            [node.model_dump_json() for node in self.logic_nodes_to_process]
        )


class ChapterBlueprintBrainstormContext(ChapterBlueprintContext):
    chapter_blueprint: ChapterBlueprint
    history: list[str]
    user_input: str = ""

    def format_chapter_blueprint(self) -> str:
        return self.chapter_blueprint.model_dump_json()


class ChapterSceneContext(ChapterBlueprintContext):
    last_scene_beat: SceneBeat
    chapter_blueprint: ChapterBlueprint
    scene_blueprint: SceneBlueprint
