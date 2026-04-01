import pytest
from inline_snapshot import snapshot

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.outlines.context.chapter import ChapterBlueprintContext, ChapterContext
from app.modules.outlines.engines.chapter import ChapterEngine
from app.modules.outlines.schemas.bible import Bible
from app.modules.outlines.schemas.chapter import (
    ChapterBlueprint,
    ChapterOutline,
    ChapterScene,
    ChapterSceneBeat,
    ChapterSceneBlueprint,
)
from app.modules.outlines.schemas.substory import ChapterOriginalSubstoryNodes, Substory
from tests.support.llm import EngineContext


@pytest.fixture()
def chapter_blueprint_context(
    bible: Bible,
    substory: Substory,
    cumulative_substory_summary: CumulativeSubstorySummary,
    chapter_summary: ChapterSummary,
    chapter_original_substory_nodes: ChapterOriginalSubstoryNodes,
) -> ChapterBlueprintContext:
    return ChapterBlueprintContext(
        bible=bible,
        substory=substory,
        cumulative_substory_summary=cumulative_substory_summary,
        pre_chapter_summary=chapter_summary,
        logic_nodes_to_process=chapter_original_substory_nodes,
    )


@pytest.mark.integration()
@pytest.mark.asyncio()
async def test_chapter_pipeline(
    chapter_engine_context: EngineContext[ChapterEngine, ChapterBlueprint | ChapterScene],
    chapter_blueprint_context: ChapterBlueprintContext,
    chapter_outline: ChapterOutline,
):
    chapter_engine = chapter_engine_context.engine
    fake_llm = chapter_engine_context.fake_llm
    chapter_blueprint = await chapter_engine.chapter_blueprint_generate(chapter_blueprint_context)
    chapter_context = ChapterContext(
        **chapter_blueprint_context.model_dump(),
        chapter_blueprint=chapter_blueprint,
    )
    chapter = await chapter_engine.chapter_generate(chapter_context)
    assert fake_llm.structured_responses == snapshot(
        [
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
            ),
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
            ),
        ]
    )
    assert fake_llm.structured_output_requests == snapshot(
        [
            {
                "schema": ChapterBlueprint,
                "include_raw": False,
                "method": "function_calling",
                "strict": True,
            },
            {
                "schema": ChapterScene,
                "include_raw": False,
                "method": "function_calling",
                "strict": True,
            },
        ]
    )
    assert chapter == chapter_outline
