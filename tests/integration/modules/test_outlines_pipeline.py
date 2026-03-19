import pytest

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.outlines.context.chapter import ChapterContext
from app.modules.outlines.engines.bible import BibleEngine
from app.modules.outlines.engines.chapter import ChapterEngine
from app.modules.outlines.engines.substory import SubstoryEngine
from app.modules.outlines.schemas.chapter import Chapter
from app.modules.outlines.schemas.substory import ChapterOriginalSubstoryNodes


@pytest.fixture()
def bible_brainstorm_context() -> BibleEngine.BibleBrainstormContext:
    return BibleEngine.BibleBrainstormContext(history=[], user_input="这个主意就挺好的")


@pytest.mark.integration()
@pytest.mark.asyncio()
async def test_outlines_pipeline(
    bible_engine: BibleEngine,
    substory_engine: SubstoryEngine,
    chapter_engine: ChapterEngine,
    bible_brainstorm_context: BibleEngine.BibleBrainstormContext,
    cumulative_substory_summary: CumulativeSubstorySummary,
    chapter_summary: ChapterSummary,
    chapter_outline: Chapter,
) -> None:
    messages = [*bible_brainstorm_context.history, bible_brainstorm_context.user_input]
    result = await bible_engine.brainstorm(bible_brainstorm_context)
    messages = [*messages, result]
    bible_generate_context = BibleEngine.BibleGenerateContext(messages=messages)
    bible = await bible_engine.generate(bible_generate_context)

    substory_brainstorm_context = SubstoryEngine.SubstoryBrainstormContext(
        bible=bible,
        history=[],
        user_input="这个主意就挺好的",
    )
    result = await substory_engine.brainstorm(substory_brainstorm_context)
    messages = [
        *substory_brainstorm_context.history,
        substory_brainstorm_context.user_input,
        result,
    ]
    substory_generate_context = substory_engine.SubstoryGenerateContext(
        messages=messages, bible=bible
    )
    substory = await substory_engine.generate(substory_generate_context)

    chapter_blueprint_context = chapter_engine.ChapterBlueprintContext(
        bible=bible,
        substory=substory,
        cumulative_substory_summary=cumulative_substory_summary,
        pre_chapter_summary=chapter_summary,
        logic_nodes_to_process=ChapterOriginalSubstoryNodes(nodes=substory.logic_nodes),
    )
    chapter_blueprint = await chapter_engine.chapter_blueprint_generate(chapter_blueprint_context)
    chapter_context = ChapterContext(
        **chapter_blueprint_context.model_dump(),
        chapter_blueprint=chapter_blueprint,
    )
    chapter = await chapter_engine.chapter_generate(chapter_context)
    assert chapter == chapter_outline
