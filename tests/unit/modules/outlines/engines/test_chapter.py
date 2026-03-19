import pytest

from inline_snapshot import snapshot

from pytest_mock import MockerFixture
from unittest.mock import MagicMock
from app.modules.outlines.engines.chapter import ChapterEngine
from app.modules.outlines.schemas.chapter import (
    Chapter,
    ChapterBlueprint,
    ChapterScene,
    ChapterSceneBlueprint,
    ChapterSceneBeat,
)
from app.modules.outlines.context.chapter import (
    ChapterBlueprintBrainstormContext,
    ChapterBlueprintContext,
    ChapterContext,
    ChapterSceneContext,
)


@pytest.fixture()
def mock_blueprint_brainstorm_chain(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("app.modules.outlines.engines.chapter.get_chapter_brainstorm_chain")
    mock.return_value.ainvoke = mocker.AsyncMock()
    mock.return_value.ainvoke.return_value = "测试蓝图头脑风暴"
    return mock


@pytest.fixture()
def mock_blueprint_chain(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("app.modules.outlines.engines.chapter.get_chapter_blueprint_chain")
    mock.return_value.ainvoke = mocker.AsyncMock()
    mock.return_value.ainvoke.return_value = ChapterBlueprint(
        chapter_index=1,
        title="雨夜的枪声",
        thematic_tone="紧张、压抑",
        opening_hook="一颗子弹擦过李四的耳边，打碎了身后的净水器",
        ending_cliffhanger="李四倒在血泊中，眼看黑帮老大举起了枪，突然他的手心闪烁起蓝色的电光……",
        scenes_blueprint=[
            ChapterSceneBlueprint(
                location="贫民窟的废弃工厂巷道",
                time_setting="深夜，暴雨倾盆",
                characters=["李四", "黑帮小喽啰", "妹妹小红"],
                objective="李四试图带着妹妹逃离黑帮的包围圈",
                logic_bridge="承接卷一节点1：黑帮火拼爆发",
            )
        ],
    )
    return mock


@pytest.fixture()
def mock_scene_chain(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("app.modules.outlines.engines.chapter.get_chapter_scene_chain")
    mock.return_value.ainvoke = mocker.AsyncMock()
    mock.return_value.ainvoke.return_value = ChapterScene(
        location="贫民窟的废弃工厂巷道",
        time_setting="深夜，暴雨倾盆",
        characters=["李四", "黑帮小喽啰", "妹妹小红"],
        objective="李四试图带着妹妹逃离黑帮的包围圈",
        logic_bridge="承接卷一节点1：黑帮火拼爆发",
        beats=[
            ChapterSceneBeat(
                category="动作",
                mood="激昂",
                description="李四翻滚躲开射击，同时抛出一枚自制电磁脉冲手雷",
            )
        ],
    )
    return mock


@pytest.fixture()
def chapter_engine(
    mock_blueprint_brainstorm_chain: MagicMock,
    mock_blueprint_chain: MagicMock,
    mock_scene_chain: MagicMock,
) -> ChapterEngine:
    return ChapterEngine()


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_chapter_engine_brainstorm(
    chapter_engine: ChapterEngine,
    chapter_blueprint_brainstorm_context: ChapterBlueprintBrainstormContext,
    mock_blueprint_brainstorm_chain: MagicMock,
) -> None:
    result = await chapter_engine.chapter_blueprint_brainstorm(chapter_blueprint_brainstorm_context)
    variables = chapter_engine.chapter_blueprint_brainstorm_template.build_variables(
        chapter_blueprint_brainstorm_context
    )
    assert result == snapshot("测试蓝图头脑风暴")
    mock_blueprint_brainstorm_chain.return_value.ainvoke.assert_called_once_with(variables)


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_chapter_engine_generate_blueprint(
    chapter_engine: ChapterEngine,
    chapter_blueprint_context: ChapterBlueprintContext,
    mock_blueprint_chain: MagicMock,
) -> None:
    result = await chapter_engine.chapter_blueprint_generate(chapter_blueprint_context)
    variables = chapter_engine.chapter_blueprint_template.build_variables(chapter_blueprint_context)
    assert result == snapshot(
        ChapterBlueprint(
            chapter_index=1,
            title="雨夜的枪声",
            thematic_tone="紧张、压抑",
            opening_hook="一颗子弹擦过李四的耳边，打碎了身后的净水器",
            ending_cliffhanger="李四倒在血泊中，眼看黑帮老大举起了枪，突然他的手心闪烁起蓝色的电光……",
            scenes_blueprint=[
                ChapterSceneBlueprint(
                    location="贫民窟的废弃工厂巷道",
                    time_setting="深夜，暴雨倾盆",
                    characters=["李四", "黑帮小喽啰", "妹妹小红"],
                    objective="李四试图带着妹妹逃离黑帮的包围圈",
                    logic_bridge="承接卷一节点1：黑帮火拼爆发",
                )
            ],
        )
    )
    mock_blueprint_chain.return_value.ainvoke.assert_called_once_with(variables)


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_chapter_engine_generate_scene(
    chapter_engine: ChapterEngine,
    chapter_scene_context: ChapterSceneContext,
    mock_scene_chain: MagicMock,
) -> None:
    result = await chapter_engine.chapter_scene_generate(chapter_scene_context)
    variables = chapter_engine.chapter_scene_template.build_variables(chapter_scene_context)
    assert result == snapshot(
        ChapterScene(
            location="贫民窟的废弃工厂巷道",
            time_setting="深夜，暴雨倾盆",
            characters=["李四", "黑帮小喽啰", "妹妹小红"],
            objective="李四试图带着妹妹逃离黑帮的包围圈",
            logic_bridge="承接卷一节点1：黑帮火拼爆发",
            beats=[
                ChapterSceneBeat(
                    category="动作",
                    mood="激昂",
                    description="李四翻滚躲开射击，同时抛出一枚自制电磁脉冲手雷",
                )
            ],
        )
    )
    mock_scene_chain.return_value.ainvoke.assert_called_once_with(variables)


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_chapter_engine_generate_chapter(
    chapter_engine: ChapterEngine,
    chapter_context: ChapterContext,
    mock_scene_chain: MagicMock,
    chapter_scene: ChapterScene,
) -> None:
    result = await chapter_engine.chapter_generate(chapter_context)
    assert result == snapshot(
        Chapter(
            chapter_index=1,
            title="雨夜的枪声",
            thematic_tone="紧张、压抑",
            opening_hook="一颗子弹擦过李四的耳边，打碎了身后的净水器",
            ending_cliffhanger="李四倒在血泊中，眼看黑帮老大举起了枪，突然他的手心闪烁起蓝色的电光……",
            scenes=[
                ChapterScene(
                    location="贫民窟的废弃工厂巷道",
                    time_setting="深夜，暴雨倾盆",
                    characters=["李四", "黑帮小喽啰", "妹妹小红"],
                    objective="李四试图带着妹妹逃离黑帮的包围圈",
                    logic_bridge="承接卷一节点1：黑帮火拼爆发",
                    beats=[
                        ChapterSceneBeat(
                            category="动作",
                            mood="激昂",
                            description="李四翻滚躲开射击，同时抛出一枚自制电磁脉冲手雷",
                        )
                    ],
                )
            ],
        )
    )
