import pytest
from inline_snapshot import snapshot
from pytest_mock import MockerFixture

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.outlines.schemas.bible import Bible
from app.modules.outlines.schemas.chapter import Chapter as ChapterOutline
from app.modules.outlines.schemas.substory import ChapterOriginalSubstoryNodes, Substory
from app.modules.post_writing.engine import PostWritingEngine
from app.modules.writing.schemas import Chapter, SceneChunk


@pytest.fixture()
def chapter() -> Chapter:
    return Chapter(
        chunks=[
            SceneChunk(content="第一场戏内容。"),
            SceneChunk(content="第二场戏内容。"),
        ]
    )


@pytest.fixture()
def post_writing_engine(mocker: MockerFixture) -> PostWritingEngine:
    summary_chain = mocker.patch("app.modules.post_writing.engine.get_chapter_summary_chain")
    summary_chain.return_value.ainvoke = mocker.AsyncMock(return_value="这是本章的剧情梗概")

    cumulative_summary_chain = mocker.patch(
        "app.modules.post_writing.engine.get_cumulative_substory_summary_chain"
    )
    cumulative_summary_chain.return_value.ainvoke = mocker.AsyncMock(
        return_value="这是本卷的累计剧情梗概"
    )
    return PostWritingEngine()


@pytest.mark.integration()
@pytest.mark.asyncio()
async def test_post_writing_pipeline(
    post_writing_engine: PostWritingEngine,
    cumulative_substory_summary: CumulativeSubstorySummary,
    chapter_summary: ChapterSummary,
    bible: Bible,
    substory: Substory,
    chapter_original_substory_nodes: ChapterOriginalSubstoryNodes,
    chapter_outline: ChapterOutline,
    chapter: Chapter,
) -> None:
    current_chapter_summary = await post_writing_engine.chapter_summary(
        post_writing_engine.ChapterSummaryContext(
            bible=bible,
            substory=substory,
            original_logic_nodes=chapter_original_substory_nodes,
            chapter_outline=chapter_outline,
            cumulative_substory_summary=cumulative_substory_summary,
            pre_chapter_summary=chapter_summary,
            chapter=chapter,
        )
    )

    assert current_chapter_summary.summary == snapshot("这是本章的剧情梗概")

    cumulative_substory_summary = await post_writing_engine.cumulative_substory_summary(
        post_writing_engine.SubstoryCumulativeSummaryContext(
            bible=bible,
            substory=substory,
            cumulative_substory_summary=cumulative_substory_summary,
            current_chapter_summary=current_chapter_summary,
        )
    )

    assert cumulative_substory_summary.summary == snapshot("这是本卷的累计剧情梗概")
