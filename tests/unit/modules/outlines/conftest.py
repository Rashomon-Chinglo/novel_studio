import pytest

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
    SubstoryActionNode,
)
from app.modules.outlines.context.bible import BibleBrainstormContext, BibleGenerateContext
from app.modules.outlines.context.substory import SubstoryBrainstormContext, SubstoryGenerateContext
from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.outlines.context.chapter import ChapterBlueprintContext, ChapterBlueprintBrainstormContext, ChapterSceneContext, ChapterContext

@pytest.fixture
def chapter_summary() -> ChapterSummary:
    return ChapterSummary(summary="上一章讲了李四逃入废弃工厂，暂时躲过了追捕。")

@pytest.fixture
def cumulative_substory_summary() -> CumulativeSubstorySummary:
    return CumulativeSubstorySummary(summary="黑帮大举搜索贫民窟，李四处于极度恐惧中。")


@pytest.fixture
def bible() -> Bible:
    return Bible(
        title="测试小说名",
        logline="这是一个测试用的核心梗概，描述了主角的冒险故事。",
        marketing_hook="无敌流，快节奏，系统文",
        worldview_tone="赛博朋克风格废土世界，基调灰暗但充满希望",
        main_conflict="底层平民与财阀高层的生存资源争夺战",
        ending_vision="主角推翻财阀，建立新的秩序",
        key_roles_summary="主角李四是孤儿，配角王五是他的黑客导师",
    )


@pytest.fixture
def substory_action_node() -> SubstoryActionNode:
    return SubstoryActionNode(
        cause="黑帮抢夺贫民窟的净水装置",
        process="主角为了保护妹妹被卷入冲突，意外接触到神秘源石",
        effect="主角觉醒了雷电异能",
        exchange="平静的生活被打破，被黑帮追杀",
        context="此时全城的警方力量已被财阀抽走",
    )


@pytest.fixture
def substory(substory_action_node: SubstoryActionNode) -> Substory:
    return Substory(
        substory_title="第一卷：初入废土",
        core_conflict="主角能否在贫民窟的黑帮火拼中活下来",
        status_change="从手无寸铁的平民变为觉醒异能的战士",
        logic_nodes=[substory_action_node],
    )


@pytest.fixture
def chapter_original_substory_nodes(
    substory_action_node: SubstoryActionNode,
) -> ChapterOriginalSubstoryNodes:
    return ChapterOriginalSubstoryNodes(
        nodes=[substory_action_node]
    )


@pytest.fixture
def chapter_scene_beat() -> ChapterSceneBeat:
    return ChapterSceneBeat(
        category="动作",
        mood="激昂",
        description="李四翻滚躲开射击，同时抛出一枚自制电磁脉冲手雷",
    )


@pytest.fixture
def chapter_scene_blueprint() -> ChapterSceneBlueprint:
    return ChapterSceneBlueprint(
        location="贫民窟的废弃工厂巷道",
        time_setting="深夜，暴雨倾盆",
        characters=["李四", "黑帮小喽啰", "妹妹小红"],
        objective="李四试图带着妹妹逃离黑帮的包围圈",
        logic_bridge="承接卷一节点1：黑帮火拼爆发",
    )


@pytest.fixture
def chapter_scene(
    chapter_scene_blueprint: ChapterSceneBlueprint,
    chapter_scene_beat: ChapterSceneBeat,
) -> ChapterScene:
    return ChapterScene(
        **chapter_scene_blueprint.model_dump(),
        beats=[chapter_scene_beat],
    )


@pytest.fixture
def chapter_blueprint(
    chapter_scene_blueprint: ChapterSceneBlueprint,
) -> ChapterBlueprint:
    return ChapterBlueprint(
        chapter_index=1,
        title="雨夜的枪声",
        thematic_tone="紧张、压抑",
        opening_hook="一颗子弹擦过李四的耳边，打碎了身后的净水器",
        ending_cliffhanger="李四倒在血泊中，眼看黑帮老大举起了枪，突然他的手心闪烁起蓝色的电光……",
        scenes_blueprint=[chapter_scene_blueprint],
    )


@pytest.fixture
def chapter(
    chapter_blueprint: ChapterBlueprint,
    chapter_scene: ChapterScene,
) -> Chapter:
    data = chapter_blueprint.model_dump(exclude={"scenes_blueprint"})
    return Chapter(
        **data,
        scenes=[chapter_scene],
    )

@pytest.fixture
def history() -> list[str]:
    return ["test", "history"]

@pytest.fixture
def user_input() -> str:
    return "test"

@pytest.fixture
def messages() -> list[str]:
    return ["test", "messages"]

@pytest.fixture
def bible_brainstorm_context(history: list[str], user_input: str) -> BibleBrainstormContext:
    return BibleBrainstormContext(
        history=history,
        user_input=user_input,
    )

@pytest.fixture
def bible_generate_context(messages: list[str]) -> BibleGenerateContext:
    return BibleGenerateContext(
        messages=messages,
    )

@pytest.fixture
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

@pytest.fixture
def substory_generate_context(
    history: list[str],
    bible: Bible,
) -> SubstoryGenerateContext:
    return SubstoryGenerateContext(
        history=history,
        bible=bible,
    )

@pytest.fixture
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

@pytest.fixture
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

@pytest.fixture
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

@pytest.fixture
def chapter_context(
    chapter_blueprint_context: ChapterBlueprintContext,
    chapter_blueprint: ChapterBlueprint,
) -> ChapterContext:
    return ChapterContext(
        **chapter_blueprint_context.model_dump(),
        chapter_blueprint=chapter_blueprint,
    )
