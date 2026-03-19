import pytest
from app.modules.outlines.schemas.chapter import Chapter
from app.modules.outlines.engines.chapter import ChapterEngine
from app.modules.outlines.schemas.bible import Bible
from app.modules.outlines.context.chapter import ChapterBlueprintContext
from app.modules.outlines.context.chapter import ChapterContext
from app.modules.outlines.schemas.substory import Substory
from app.modules.base.memory import CumulativeSubstorySummary
from app.modules.base.memory import ChapterSummary
from app.modules.outlines.schemas.substory import ChapterOriginalSubstoryNodes


@pytest.fixture()
def chapter_blueprint_context(
    bible: Bible,
    substory: Substory,
    cumulative_substory_summary: CumulativeSubstorySummary,
    chapter_summary: ChapterSummary,
    chapter_original_substory_nodes: ChapterOriginalSubstoryNodes,
) -> ChapterBlueprintContext:
    return ChapterBlueprintContext(
        bible=bible,
        substory=substory,
        cumulative_substory_summary=cumulative_substory_summary,
        pre_chapter_summary=chapter_summary,
        logic_nodes_to_process=chapter_original_substory_nodes,
    )


@pytest.mark.integration()
@pytest.mark.asyncio()
async def test_chapter_pipeline(
    chapter_engine: ChapterEngine,
    chapter_blueprint_context: ChapterBlueprintContext,
    chapter_outline: Chapter,
):
    chapter_blueprint = await chapter_engine.chapter_blueprint_generate(chapter_blueprint_context)
    chapter_context = ChapterContext(
        **chapter_blueprint_context.model_dump(),
        chapter_blueprint=chapter_blueprint,
    )
    chapter = await chapter_engine.chapter_generate(chapter_context)
    assert chapter == chapter_outline
