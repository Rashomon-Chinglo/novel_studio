from unittest.mock import MagicMock

import pytest
from inline_snapshot import snapshot
from pytest_mock import MockerFixture

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.post_writing.context import ChapterSummaryContext, SubstoryCumulativeSummaryContext
from app.modules.post_writing.engine import PostWritingEngine


@pytest.fixture()
def mock_chapter_summary_chain(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("app.modules.post_writing.engine.get_chapter_summary_chain")
    mock.return_value.ainvoke = mocker.AsyncMock()
    mock.return_value.ainvoke.return_value = "测试章节总结"
    return mock


@pytest.fixture()
def mock_substory_cumulative_summary_chain(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("app.modules.post_writing.engine.get_cumulative_substory_summary_chain")
    mock.return_value.ainvoke = mocker.AsyncMock()
    mock.return_value.ainvoke.return_value = "测试累积总结"
    return mock


@pytest.fixture()
def post_writing_engine(
    mock_chapter_summary_chain: MagicMock,
    mock_substory_cumulative_summary_chain: MagicMock,
) -> PostWritingEngine:
    return PostWritingEngine()


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_post_writing_engine_chapter_summary(
    post_writing_engine: PostWritingEngine,
    chapter_summary_context: ChapterSummaryContext,
    mock_chapter_summary_chain: MagicMock,
) -> None:
    result = await post_writing_engine.chapter_summary(chapter_summary_context)

    assert result == snapshot(ChapterSummary(summary="测试章节总结"))

    variables = post_writing_engine.chapter_summary_prompt.build_variables(chapter_summary_context)
    mock_chapter_summary_chain.return_value.ainvoke.assert_called_once_with(variables)


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_post_writing_engine_cumulative_substory_summary(
    post_writing_engine: PostWritingEngine,
    substory_cumulative_summary_context: SubstoryCumulativeSummaryContext,
    mock_substory_cumulative_summary_chain: MagicMock,
) -> None:
    result = await post_writing_engine.cumulative_substory_summary(
        substory_cumulative_summary_context
    )

    assert result == snapshot(CumulativeSubstorySummary(summary="测试累积总结"))

    variables = post_writing_engine.substory_cumulative_summary_prompt.build_variables(
        substory_cumulative_summary_context
    )
    mock_substory_cumulative_summary_chain.return_value.ainvoke.assert_called_once_with(variables)
