import pytest

from app.modules.materials.engine import MaterialEngine
from app.modules.materials.schemas import ExtractedResult, MaterialSnippet


@pytest.fixture()
def mock_chain(mocker):
    mock = mocker.patch("app.modules.materials.engine.get_mining_chain")
    mock.return_value.ainvoke = mocker.AsyncMock()
    return mock


@pytest.fixture()
def engine(mock_chain):
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
def test_engine_split_text(engine, text, length_of_chunks):
    chunks = engine.split_text(text)
    assert len(chunks) == length_of_chunks


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_engine_mine(engine, mock_chain):
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
