import pytest
from inline_snapshot import snapshot
from unittest.mock import AsyncMock, patch, MagicMock

from app.modules.writing.engine import WritingEngine
from app.modules.writing.context import ChapterSceneWritingContext, ChapterWritingContext
from app.modules.writing.schemas import Chapter, SceneChunk
from app.modules.writing.providers import MaterialProvider


@pytest.fixture()
def mock_scene_writing_chain(mocker: MagicMock) -> MagicMock:
    mock = mocker.patch("app.modules.writing.engine.get_scene_writing_chain")
    mock.return_value.ainvoke = mocker.AsyncMock()
    mock.return_value.ainvoke.return_value = "测试场景写作"
    return mock


@pytest.fixture()
def writing_engine(
    material_provider: MaterialProvider, mock_scene_writing_chain: MagicMock
) -> WritingEngine:
    return WritingEngine(material_provider=material_provider)


@pytest.mark.asyncio
@pytest.mark.unit()
async def test_scene_writing(
    writing_engine: WritingEngine,
    chapter_scene_writing_context: ChapterSceneWritingContext,
    mock_scene_writing_chain: MagicMock,
) -> None:
    result = await writing_engine.scene_writing(chapter_scene_writing_context)
    assert result == snapshot(SceneChunk(content="测试场景写作"))
    mock_scene_writing_chain.return_value.ainvoke.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.unit()
async def test_writing(
    writing_engine: WritingEngine,
    chapter_writing_context: ChapterWritingContext,
    material_provider: MaterialProvider,
    mock_scene_writing_chain: MagicMock,
) -> None:
    # Mocking scene_writing to avoid deep chain mocking
    mock_scene_writing_chain.return_value.ainvoke.side_effect = ["第一场戏内容。"]

    result = await writing_engine.writing(chapter_writing_context)

    assert result == snapshot(Chapter(chunks=[SceneChunk(content="第一场戏内容。")]))
