import pytest

from unittest.mock import MagicMock
from pytest_mock import MockerFixture
from app.modules.materials.engine import MaterialEngine
from app.modules.materials.schemas import ExtractedResult, MaterialSnippet


@pytest.fixture()
def mock_chain(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("app.modules.materials.engine.get_mining_chain")
    mock.return_value.ainvoke = mocker.AsyncMock()
    return mock


@pytest.fixture()
def engine(mock_chain: MagicMock) -> MaterialEngine:
    return MaterialEngine()


@pytest.mark.unit()
@pytest.mark.parametrize(
    ("text", "length_of_chunks"),
    [
        ("", 0),
        ("你好，你今天晚上吃什么？", 1),
        ("你好，你今天晚上吃什么？" * 50, 2),
    ],
)
def test_engine_split_text(engine: MaterialEngine, text: str, length_of_chunks: int) -> None:
    chunks = engine.split_text(text)
    assert len(chunks) == length_of_chunks


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_engine_mine(engine: MaterialEngine, mock_chain: MagicMock) -> None:
    mock_response = ExtractedResult(
        snippets=[
            MaterialSnippet(
                essential_text="现代化 Mock 提取的内容",
                category="心理",
                mood="愤怒",
                tags=["pytest-mock"],
            )
        ]
    )

    mock_chain.return_value.ainvoke.return_value = mock_response

    context = MaterialEngine.MaterialsMiningContext(text="test")
    result = await engine.mine(context)

    assert result == mock_response
    mock_chain.return_value.ainvoke.assert_called_once_with({"text": "test"})
