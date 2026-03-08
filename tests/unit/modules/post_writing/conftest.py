import pytest
from app.modules.outlines.schemas.bible import Bible
from app.modules.outlines.schemas.chapter import Chapter as ChapterOutline
from app.modules.outlines.schemas.substory import ChapterOriginalSubstoryNodes, Substory
from app.modules.writing.schemas import Chapter as WritingChapter, SceneChunk
from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.post_writing.context import ChapterSummaryContext, SubstoryCumulativeSummaryContext

@pytest.fixture()
def writing_chapter() -> WritingChapter:
    return WritingChapter(
        chunks=[
            SceneChunk(content="李四喘着粗气，靠在冰冷的墙上。"),
            SceneChunk(content="外面传来了杂乱的脚步声。")
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
    writing_chapter: WritingChapter,
) -> ChapterSummaryContext:
    return ChapterSummaryContext(
        bible=bible,
        substory=substory,
        original_logic_nodes=chapter_original_substory_nodes,
        chapter_outline=chapter_outline,
        cumulative_substory_summary=cumulative_substory_summary,
        pre_chapter_summary=chapter_summary,
        chapter=writing_chapter,
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
