import pytest

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.outlines.schemas.bible import Bible
from app.modules.outlines.schemas.chapter import ChapterOutline
from app.modules.outlines.schemas.substory import ChapterOriginalSubstoryNodes, Substory
from app.modules.post_writing.context import ChapterSummaryContext, SubstoryCumulativeSummaryContext
from app.modules.writing.schemas import SceneChunk, WrittenChapter


@pytest.fixture()
def written_chapter() -> WrittenChapter:
    return WrittenChapter(
        chunks=[
            SceneChunk(content="李四喘着粗气，靠在冰冷的墙上。"),
            SceneChunk(content="外面传来了杂乱的脚步声。"),
        ]
    )


@pytest.fixture()
def chapter_summary_context(
    bible: Bible,
    substory: Substory,
    chapter_original_substory_nodes: ChapterOriginalSubstoryNodes,
    chapter_outline: ChapterOutline,
    cumulative_substory_summary: CumulativeSubstorySummary,
    chapter_summary: ChapterSummary,
    written_chapter: WrittenChapter,
) -> ChapterSummaryContext:
    return ChapterSummaryContext(
        bible=bible,
        substory=substory,
        original_logic_nodes=chapter_original_substory_nodes,
        chapter_outline=chapter_outline,
        cumulative_substory_summary=cumulative_substory_summary,
        pre_chapter_summary=chapter_summary,
        written_chapter=written_chapter,
    )


@pytest.fixture()
def substory_cumulative_summary_context(
    bible: Bible,
    substory: Substory,
    cumulative_substory_summary: CumulativeSubstorySummary,
    chapter_summary: ChapterSummary,
) -> SubstoryCumulativeSummaryContext:
    return SubstoryCumulativeSummaryContext(
        bible=bible,
        substory=substory,
        cumulative_substory_summary=cumulative_substory_summary,
        current_chapter_summary=chapter_summary,
    )
