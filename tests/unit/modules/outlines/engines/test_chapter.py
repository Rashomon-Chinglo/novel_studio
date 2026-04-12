import pytest
from inline_snapshot import snapshot
from pytest_mock import MockerFixture

from app.modules.outlines.context.chapter import (
    ChapterBlueprintContext,
    ChapterContext,
    ChapterSceneContext,
)
from app.modules.outlines.engines.chapter import ChapterEngine
from app.modules.outlines.schemas.chapter import (
    ChapterBlueprint,
    ChapterOutline,
    ChapterScene,
    ChapterSceneBeat,
    ChapterSceneBlueprint,
)
from tests.support.llm import EngineContext, FakeLLMFactory


@pytest.fixture()
def blueprint_engine_context(
    mocker: MockerFixture,
    fake_llm_factory: FakeLLMFactory,
    chapter_blueprint: ChapterBlueprint,
) -> EngineContext[ChapterEngine, ChapterBlueprint]:
    fake_llm = fake_llm_factory(
        structured_responses=[chapter_blueprint],
    )
    mocker.patch("app.modules.outlines.chain.chapter.get_llm", return_value=fake_llm)
    engine = ChapterEngine()
    return EngineContext(engine=engine, fake_llm=fake_llm)


@pytest.fixture()
def scene_engine_context(
    mocker: MockerFixture,
    fake_llm_factory: FakeLLMFactory,
    chapter_scene: ChapterScene,
) -> EngineContext[ChapterEngine, ChapterScene]:
    fake_llm = fake_llm_factory(
        structured_responses=[chapter_scene],
    )
    mocker.patch("app.modules.outlines.chain.chapter.get_llm", return_value=fake_llm)
    engine = ChapterEngine()
    return EngineContext(engine=engine, fake_llm=fake_llm)


@pytest.fixture()
def chapter_engine_context(
    mocker: MockerFixture,
    fake_llm_factory: FakeLLMFactory,
    chapter_scene: ChapterScene,
) -> EngineContext[ChapterEngine, ChapterScene]:
    fake_llm = fake_llm_factory(
        structured_responses=[chapter_scene],
    )
    mocker.patch("app.modules.outlines.chain.chapter.get_llm", return_value=fake_llm)
    engine = ChapterEngine()
    return EngineContext(engine=engine, fake_llm=fake_llm)


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_chapter_engine_generate_blueprint(
    blueprint_engine_context: EngineContext[ChapterEngine, ChapterBlueprint],
    chapter_blueprint_context: ChapterBlueprintContext,
    chapter_blueprint: ChapterBlueprint,
) -> None:
    chapter_engine = blueprint_engine_context.engine
    fake_llm = blueprint_engine_context.fake_llm

    result = await chapter_engine.chapter_blueprint_generate(chapter_blueprint_context)

    assert result == snapshot(
        ChapterBlueprint(
            chapter_index=1,
            substory_chapter_index=1,
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
    assert fake_llm.structured_output_requests == snapshot(
        [
            {
                "schema": ChapterBlueprint,
                "include_raw": False,
                "method": "function_calling",
                "strict": True,
            }
        ]
    )
    assert chapter_blueprint_context.logic_nodes_to_process.nodes[0].cause in "\n".join(
        fake_llm.structured_prompts[0]
    )


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_chapter_engine_generate_scene(
    scene_engine_context: EngineContext[ChapterEngine, ChapterScene],
    chapter_scene_context: ChapterSceneContext,
    chapter_scene: ChapterScene,
) -> None:
    chapter_engine = scene_engine_context.engine
    fake_llm = scene_engine_context.fake_llm

    result = await chapter_engine.chapter_scene_generate(chapter_scene_context)

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
    assert fake_llm.structured_output_requests == snapshot(
        [
            {
                "schema": ChapterScene,
                "include_raw": False,
                "method": "function_calling",
                "strict": True,
            }
        ]
    )
    assert chapter_scene_context.scene_blueprint.location in "\n".join(
        fake_llm.structured_prompts[0]
    )


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_chapter_engine_generate_chapter(
    chapter_engine_context: EngineContext[ChapterEngine, ChapterScene],
    chapter_context: ChapterContext,
) -> None:
    chapter_engine = chapter_engine_context.engine
    fake_llm = chapter_engine_context.fake_llm

    result = await chapter_engine.chapter_generate(chapter_context)

    assert result == snapshot(
        ChapterOutline(
            chapter_index=1,
            substory_chapter_index=1,
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
    assert fake_llm.structured_output_requests == snapshot(
        [
            {
                "schema": ChapterScene,
                "include_raw": False,
                "method": "function_calling",
                "strict": True,
            }
        ]
    )
    assert chapter_context.chapter_blueprint.scenes_blueprint[0].location in "\n".join(
        fake_llm.structured_prompts[0]
    )
