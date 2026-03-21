import pytest
from inline_snapshot import snapshot
from pytest_mock import MockerFixture

from app.modules.outlines.context.bible import BibleBrainstormContext, BibleGenerateContext
from app.modules.outlines.engines.bible import BibleEngine
from app.modules.outlines.schemas import Bible
from tests.support.llm import EngineContext, FakeLLMFactory


@pytest.fixture()
def bible_engine_context(
    mocker: MockerFixture, fake_llm_factory: FakeLLMFactory
) -> EngineContext[BibleEngine, Bible]:
    fake_llm = fake_llm_factory(
        text_responses=["测试头脑风暴"],
        structured_responses=[
            Bible(
                title="测试小说名",
                logline="这是一个测试用的核心梗概，描述了主角的冒险故事。",
                marketing_hook="无敌流，快节奏，系统文",
                worldview_tone="赛博朋克风格废土世界，基调灰暗但充满希望",
                main_conflict="底层平民与财阀高层的生存资源争夺战",
                ending_vision="主角推翻财阀，建立新的秩序",
                key_roles_summary="主角李四是孤儿，配角王五是他的黑客导师",
            )
        ],
    )
    mocker.patch("app.modules.outlines.chain.bible.get_llm", return_value=fake_llm)
    return EngineContext(engine=BibleEngine(), fake_llm=fake_llm)


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_bible_engine_brainstorm(
    bible_engine_context: EngineContext[BibleEngine, Bible],
    bible_brainstorm_context: BibleBrainstormContext,
) -> None:
    bible_engine = bible_engine_context.engine
    fake_llm = bible_engine_context.fake_llm
    result = await bible_engine.brainstorm(bible_brainstorm_context)
    bible_engine.brainstorm_template.build_variables(bible_brainstorm_context)
    assert result == snapshot("测试头脑风暴")
    assert bible_brainstorm_context.user_input in "\n".join(fake_llm.plain_prompts[0])


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_bible_engine_generate(
    bible_engine_context: EngineContext[BibleEngine, Bible],
    bible_generate_context: BibleGenerateContext,
) -> None:
    bible_engine = bible_engine_context.engine
    fake_llm = bible_engine_context.fake_llm
    result = await bible_engine.generate(bible_generate_context)
    bible_engine.bible_template.build_variables(bible_generate_context)
    assert result == snapshot(
        Bible(
            title="测试小说名",
            logline="这是一个测试用的核心梗概，描述了主角的冒险故事。",
            marketing_hook="无敌流，快节奏，系统文",
            worldview_tone="赛博朋克风格废土世界，基调灰暗但充满希望",
            main_conflict="底层平民与财阀高层的生存资源争夺战",
            ending_vision="主角推翻财阀，建立新的秩序",
            key_roles_summary="主角李四是孤儿，配角王五是他的黑客导师",
        )
    )
    assert fake_llm.structured_output_requests == snapshot(
        [{"schema": Bible, "include_raw": False, "method": "function_calling", "strict": True}]
    )
