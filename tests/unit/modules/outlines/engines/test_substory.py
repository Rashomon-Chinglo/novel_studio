import pytest

from pytest_mock import MockerFixture
from unittest.mock import MagicMock
from inline_snapshot import snapshot

from app.modules.outlines.engines.substory import SubstoryEngine
from app.modules.outlines.schemas.substory import Substory, SubstoryActionNode
from app.modules.outlines.context.substory import SubstoryBrainstormContext, SubstoryGenerateContext


@pytest.fixture()
def mock_brainstorm_chain(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("app.modules.outlines.engines.substory.get_brainstorm_chain")
    mock.return_value.ainvoke = mocker.AsyncMock()
    mock.return_value.ainvoke.return_value = "测试头脑风暴"
    return mock


@pytest.fixture()
def mock_substory_chain(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("app.modules.outlines.engines.substory.get_substory_chain")
    mock.return_value.ainvoke = mocker.AsyncMock()
    mock.return_value.ainvoke.return_value = Substory(
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
    return mock


@pytest.fixture()
def substory_engine(
    mock_brainstorm_chain: MagicMock, mock_substory_chain: MagicMock
) -> SubstoryEngine:
    return SubstoryEngine()


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_substory_engine_brainstorm(
    substory_engine: SubstoryEngine,
    substory_brainstorm_context: SubstoryBrainstormContext,
    mock_brainstorm_chain: MagicMock,
) -> None:
    result = await substory_engine.brainstorm(substory_brainstorm_context)
    variables = substory_engine.brainstorm_template.build_variables(substory_brainstorm_context)
    assert result == snapshot("测试头脑风暴")
    mock_brainstorm_chain.return_value.ainvoke.assert_called_once_with(variables)


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_substory_engine_generate(
    substory_engine: SubstoryEngine,
    substory_generate_context: SubstoryGenerateContext,
    mock_substory_chain: MagicMock,
) -> None:
    result = await substory_engine.generate(substory_generate_context)
    variables = substory_engine.substory_template.build_variables(substory_generate_context)
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
    mock_substory_chain.return_value.ainvoke.assert_called_once_with(variables)
