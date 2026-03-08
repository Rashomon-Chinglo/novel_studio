import pytest
from inline_snapshot import snapshot
from pytest_mock import MockerFixture
from unittest.mock import MagicMock
from app.modules.outlines.schemas import Bible
from app.modules.outlines.engines.bible import BibleEngine
from app.modules.outlines.context.bible import BibleBrainstormContext, BibleGenerateContext


@pytest.fixture()
def mock_brainstorm_chain(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("app.modules.outlines.engines.bible.get_brainstorm_chain")
    mock.return_value.ainvoke = mocker.AsyncMock()
    mock.return_value.ainvoke.return_value = "测试头脑风暴"
    return mock


@pytest.fixture()
def mock_bible_chain(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("app.modules.outlines.engines.bible.get_bible_chain")
    mock.return_value.ainvoke = mocker.AsyncMock()
    mock.return_value.ainvoke.return_value = Bible(
        title="测试小说名",
        logline="这是一个测试用的核心梗概，描述了主角的冒险故事。",
        marketing_hook="无敌流，快节奏，系统文",
        worldview_tone="赛博朋克风格废土世界，基调灰暗但充满希望",
        main_conflict="底层平民与财阀高层的生存资源争夺战",
        ending_vision="主角推翻财阀，建立新的秩序",
        key_roles_summary="主角李四是孤儿，配角王五是他的黑客导师",
    )
    return mock


@pytest.fixture()
def bible_engine(mock_brainstorm_chain: MagicMock, mock_bible_chain: MagicMock) -> BibleEngine:
    return BibleEngine()


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_bible_engine_brainstorm(
    bible_engine: BibleEngine,
    bible_brainstorm_context: BibleBrainstormContext,
    mock_brainstorm_chain: MagicMock,
) -> None:
    result = await bible_engine.brainstorm(bible_brainstorm_context)
    variables = bible_engine.brainstorm_template.build_variables(bible_brainstorm_context)
    assert result == snapshot("测试头脑风暴")
    mock_brainstorm_chain.return_value.ainvoke.assert_called_once_with(variables)


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_bible_engine_generate(
    bible_engine: BibleEngine,
    bible_generate_context: BibleGenerateContext,
    mock_bible_chain: MagicMock,
) -> None:
    result = await bible_engine.generate(bible_generate_context)
    variables = bible_engine.bible_template.build_variables(bible_generate_context)
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
    mock_bible_chain.return_value.ainvoke.assert_called_once_with(variables)
