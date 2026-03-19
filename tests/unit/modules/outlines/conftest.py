import pytest

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.outlines.context.bible import BibleBrainstormContext, BibleGenerateContext
from app.modules.outlines.context.chapter import (
    ChapterBlueprintBrainstormContext,
    ChapterBlueprintContext,
    ChapterContext,
    ChapterSceneContext,
)
from app.modules.outlines.context.substory import SubstoryBrainstormContext, SubstoryGenerateContext
from app.modules.outlines.schemas.bible import Bible
from app.modules.outlines.schemas.chapter import (
    Chapter,
    ChapterBlueprint,
    ChapterScene,
    ChapterSceneBeat,
    ChapterSceneBlueprint,
)
from app.modules.outlines.schemas.substory import (
    ChapterOriginalSubstoryNodes,
    Substory,
)


@pytest.fixture()
def history() -> list[str]:
    return ["chat_history_1", "chat_history_2"]


@pytest.fixture()
def user_input() -> str:
    return "user_input"


@pytest.fixture()
def messages(history: list[str], user_input: str) -> list[str]:
    return [*history, user_input]


@pytest.fixture()
def bible_brainstorm_context(history: list[str], user_input: str) -> BibleBrainstormContext:
    return BibleBrainstormContext(
        history=history,
        user_input=user_input,
    )


@pytest.fixture()
def bible_generate_context(messages: list[str]) -> BibleGenerateContext:
    return BibleGenerateContext(
        messages=messages,
    )


@pytest.fixture()
def substory_brainstorm_context(
    history: list[str],
    user_input: str,
    bible: Bible,
) -> SubstoryBrainstormContext:
    return SubstoryBrainstormContext(
        history=history,
        user_input=user_input,
        bible=bible,
    )


@pytest.fixture()
def substory_generate_context(
    messages: list[str],
    bible: Bible,
) -> SubstoryGenerateContext:
    return SubstoryGenerateContext(
        messages=messages,
        bible=bible,
    )


@pytest.fixture()
def chapter_blueprint_context(
    bible: Bible,
    substory: Substory,
    chapter_summary: ChapterSummary,
    cumulative_substory_summary: CumulativeSubstorySummary,
    chapter_original_substory_nodes: ChapterOriginalSubstoryNodes,
) -> ChapterBlueprintContext:
    return ChapterBlueprintContext(
        bible=bible,
        substory=substory,
        pre_chapter_summary=chapter_summary,
        cumulative_substory_summary=cumulative_substory_summary,
        logic_nodes_to_process=chapter_original_substory_nodes,
    )


@pytest.fixture()
def chapter_blueprint_brainstorm_context(
    chapter_blueprint_context: ChapterBlueprintContext,
    chapter_blueprint: ChapterBlueprint,
    history: list[str],
    user_input: str,
) -> ChapterBlueprintBrainstormContext:
    return ChapterBlueprintBrainstormContext(
        **chapter_blueprint_context.model_dump(),
        chapter_blueprint=chapter_blueprint,
        history=history,
        user_input=user_input,
    )


@pytest.fixture()
def chapter_scene_context(
    chapter_blueprint_context: ChapterBlueprintContext,
    chapter_scene_beat: ChapterSceneBeat,
    chapter_blueprint: ChapterBlueprint,
    chapter_scene_blueprint: ChapterSceneBlueprint,
) -> ChapterSceneContext:
    return ChapterSceneContext(
        **chapter_blueprint_context.model_dump(),
        last_scene_beat=chapter_scene_beat,
        chapter_blueprint=chapter_blueprint,
        scene_blueprint=chapter_scene_blueprint,
    )


@pytest.fixture()
def chapter_context(
    chapter_blueprint_context: ChapterBlueprintContext,
    chapter_blueprint: ChapterBlueprint,
) -> ChapterContext:
    return ChapterContext(
        **chapter_blueprint_context.model_dump(),
        chapter_blueprint=chapter_blueprint,
    )


@pytest.fixture()
def chapter(
    chapter_blueprint: ChapterBlueprint,
    chapter_scene: ChapterScene,
) -> Chapter:
    data = chapter_blueprint.model_dump(exclude={"scenes_blueprint"})
    return Chapter(
        **data,
        scenes=[chapter_scene],
    )
