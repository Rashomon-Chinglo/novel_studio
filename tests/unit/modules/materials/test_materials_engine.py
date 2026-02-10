import pytest
from app.modules.materials.engine import MaterialEngine
from inline_snapshot import snapshot
from pytest_mock import AsyncMockType


@pytest.mark.unit
def test_engine_split_text():
    engine = MaterialEngine()
    text = "第一段。\n\n第二段。\n\n第三段。"
    chunks = engine.split_text(text)
    assert chunks == snapshot(
        [
            """\
第一段。

第二段。

第三段。\
"""
        ]
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_engine_mine(mocker):
    mock_response = {
        "snippets": [
            {
                "essential_text": "现代化 Mock 提取的内容",
                "category": "心理",
                "mood": "激动",
                "tags": ["pytest-mock"],
            }
        ]
    }

    mock_chain = mocker.patch("app.modules.materials.engine.get_mining_chain")
    mock_chain.return_value.ainvoke = mocker.AsyncMock(return_value=mock_response)

    engine = MaterialEngine()
    context = MaterialEngine.MaterialsMiningContext(text="test")
    result = await engine.mine(context)
    assert result.model_dump() == snapshot()
    mock_chain.return_value.ainvoke.assert_called_once_with()
