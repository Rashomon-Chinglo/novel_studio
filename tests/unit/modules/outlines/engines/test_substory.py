import pytest

from inline_snapshot import snapshot

from app.modules.outlines.engines.substory import SubstoryEngine
from app.modules.outlines.schemas.substory import Substory, SubstoryActionNode


@pytest.fixture()
def mock_brainstorm_chain(mocker):
    mock = mocker.patch("app.modules.outlines.engines.substory.get_brainstorm_chain")
    mock.return_value.ainvoke = mocker.AsyncMock()
    mock.return_value.ainvoke.return_value = "test brainstorm result"
    return mock


@pytest.fixture()
def mock_substory_chain(mocker, substory: Substory):
    mock = mocker.patch("app.modules.outlines.engines.substory.get_substory_chain")
    mock.return_value.ainvoke = mocker.AsyncMock()
    mock.return_value.ainvoke.return_value = substory
    return mock


@pytest.fixture()
def substory_engine(mock_brainstorm_chain, mock_substory_chain):
    return SubstoryEngine()


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_substory_engine_brainstorm(
    substory_engine: SubstoryEngine,
    substory_brainstorm_context: SubstoryEngine.SubstoryBrainstormContext,
    mock_brainstorm_chain,
):
    result = await substory_engine.brainstorm(substory_brainstorm_context)
    variables = substory_engine.brainstorm_template.build_variables(substory_brainstorm_context)
    assert result == snapshot("test brainstorm result")
    mock_brainstorm_chain.return_value.ainvoke.assert_called_once_with(variables)


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_substory_engine_generate(
    substory_engine: SubstoryEngine,
    substory_generate_context: SubstoryEngine.SubstoryGenerateContext,
    mock_substory_chain,
):
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
            status_change="从手无寸铁的平民变为觉醒异能的战士",
        )
    )
    mock_substory_chain.return_value.ainvoke.assert_called_once_with(variables)
