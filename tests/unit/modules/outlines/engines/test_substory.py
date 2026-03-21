import pytest
from inline_snapshot import snapshot
from pytest_mock import MockerFixture

from app.modules.outlines.context.substory import SubstoryBrainstormContext, SubstoryGenerateContext
from app.modules.outlines.engines.substory import SubstoryEngine
from app.modules.outlines.schemas.substory import Substory, SubstoryActionNode
from tests.support.llm import EngineContext, FakeLLM, FakeLLMFactory


@pytest.fixture()
def substory_engine_context(
    mocker: MockerFixture, fake_llm_factory: FakeLLMFactory
) -> EngineContext[SubstoryEngine, Substory]:
    fake_llm: FakeLLM[Substory] = fake_llm_factory(
        text_responses=["测试头脑风暴"],
        structured_responses=[
            Substory(
                substory_title="第一卷：初入废土",
                logic_nodes=[
                    SubstoryActionNode(
                        cause="黑帮抢夺贫民窟的净水装置",
                        process="主角为了保护妹妹被卷入冲突，意外接触到神秘源石",
                        effect="主角觉醒了雷电异能",
                        exchange="平静的生活被打破，被黑帮追杀",
                        context="此时全城的警方力量已被财阀抽走",
                    )
                ],
                core_conflict="主角能否在贫民窟的黑帮火拼中活下来",
                status_change="从手无刻铁的平民变为觉醒异能的战士",
            )
        ],
    )
    mocker.patch("app.modules.outlines.chain.substory.get_llm", return_value=fake_llm)
    return EngineContext(engine=SubstoryEngine(), fake_llm=fake_llm)


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_substory_engine_brainstorm(
    substory_engine_context: EngineContext[SubstoryEngine, Substory],
    substory_brainstorm_context: SubstoryBrainstormContext,
) -> None:
    substory_engine = substory_engine_context.engine
    fake_llm = substory_engine_context.fake_llm
    result = await substory_engine.brainstorm(substory_brainstorm_context)
    substory_engine.brainstorm_template.build_variables(substory_brainstorm_context)
    assert result == snapshot("测试头脑风暴")
    assert substory_brainstorm_context.user_input in "\n".join(fake_llm.plain_prompts[0])


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_substory_engine_generate(
    substory_engine_context: EngineContext[SubstoryEngine, Substory],
    substory_generate_context: SubstoryGenerateContext,
) -> None:
    substory_engine = substory_engine_context.engine
    fake_llm = substory_engine_context.fake_llm
    result = await substory_engine.generate(substory_generate_context)
    substory_engine.substory_template.build_variables(substory_generate_context)
    assert result == snapshot(
        Substory(
            substory_title="第一卷：初入废土",
            logic_nodes=[
                SubstoryActionNode(
                    cause="黑帮抢夺贫民窟的净水装置",
                    process="主角为了保护妹妹被卷入冲突，意外接触到神秘源石",
                    effect="主角觉醒了雷电异能",
                    exchange="平静的生活被打破，被黑帮追杀",
                    context="此时全城的警方力量已被财阀抽走",
                )
            ],
            core_conflict="主角能否在贫民窟的黑帮火拼中活下来",
            status_change="从手无刻铁的平民变为觉醒异能的战士",
        )
    )
    assert fake_llm.structured_output_requests == snapshot(
        [{"schema": Substory, "include_raw": False, "method": "function_calling", "strict": True}]
    )
