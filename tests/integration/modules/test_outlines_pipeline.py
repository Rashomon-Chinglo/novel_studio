import pytest
from inline_snapshot import snapshot

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.outlines.context.chapter import ChapterContext
from app.modules.outlines.engines.bible import BibleEngine
from app.modules.outlines.engines.chapter import ChapterEngine
from app.modules.outlines.engines.substory import SubstoryEngine
from app.modules.outlines.schemas import Bible, Substory
from app.modules.outlines.schemas.chapter import Chapter, ChapterBlueprint, ChapterScene
from app.modules.outlines.schemas.substory import ChapterOriginalSubstoryNodes
from tests.support.llm import EngineContext


@pytest.fixture()
def bible_brainstorm_context() -> BibleEngine.BibleBrainstormContext:
    return BibleEngine.BibleBrainstormContext(history=[], user_input="这个主意就挺好的")


@pytest.mark.integration()
@pytest.mark.asyncio()
async def test_outlines_pipeline(
    bible_engine_context: EngineContext[BibleEngine, Bible],
    substory_engine_context: EngineContext[SubstoryEngine, Substory],
    chapter_engine_context: EngineContext[ChapterEngine, ChapterBlueprint | ChapterScene],
    bible_brainstorm_context: BibleEngine.BibleBrainstormContext,
    cumulative_substory_summary: CumulativeSubstorySummary,
    chapter_summary: ChapterSummary,
    chapter_outline: Chapter,
) -> None:
    bible_engine = bible_engine_context.engine
    substory_engine = substory_engine_context.engine
    chapter_engine = chapter_engine_context.engine
    bible_fake_llm = bible_engine_context.fake_llm
    substory_fake_llm = substory_engine_context.fake_llm
    chapter_fake_llm = chapter_engine_context.fake_llm

    messages = [*bible_brainstorm_context.history, bible_brainstorm_context.user_input]
    bible_brainstorm_result = await bible_engine.brainstorm(bible_brainstorm_context)
    assert bible_brainstorm_context.user_input in "\n".join(bible_fake_llm.plain_prompts[0])

    messages = [*messages, bible_brainstorm_result]
    bible_generate_context = BibleEngine.BibleGenerateContext(messages=messages)
    bible = await bible_engine.generate(bible_generate_context)
    assert bible_brainstorm_result in "\n".join(bible_fake_llm.structured_prompts[0])
    assert bible_fake_llm.structured_output_requests == snapshot(
        [{"schema": Bible, "include_raw": False, "method": "function_calling", "strict": True}]
    )

    substory_brainstorm_context = SubstoryEngine.SubstoryBrainstormContext(
        bible=bible,
        history=[],
        user_input="这个主意就挺好的",
    )
    substory_brainstorm_result = await substory_engine.brainstorm(substory_brainstorm_context)
    assert bible.title in "\n".join(substory_fake_llm.plain_prompts[0])

    messages = [
        *substory_brainstorm_context.history,
        substory_brainstorm_context.user_input,
        substory_brainstorm_result,
    ]
    substory_generate_context = substory_engine.SubstoryGenerateContext(
        messages=messages, bible=bible
    )
    substory = await substory_engine.generate(substory_generate_context)
    assert substory_brainstorm_result in "\n".join(substory_fake_llm.structured_prompts[0])
    assert substory_fake_llm.structured_output_requests == snapshot(
        [{"schema": Substory, "include_raw": False, "method": "function_calling", "strict": True}]
    )

    chapter_blueprint_context = chapter_engine.ChapterBlueprintContext(
        bible=bible,
        substory=substory,
        cumulative_substory_summary=cumulative_substory_summary,
        pre_chapter_summary=chapter_summary,
        logic_nodes_to_process=ChapterOriginalSubstoryNodes(nodes=substory.logic_nodes),
    )
    chapter_blueprint = await chapter_engine.chapter_blueprint_generate(chapter_blueprint_context)
    assert bible.title in "\n".join(chapter_fake_llm.structured_prompts[0])
    assert substory.substory_title in "\n".join(chapter_fake_llm.structured_prompts[0])
    assert chapter_summary.summary in "\n".join(chapter_fake_llm.structured_prompts[0])

    chapter_context = ChapterContext(
        **chapter_blueprint_context.model_dump(),
        chapter_blueprint=chapter_blueprint,
    )
    chapter = await chapter_engine.chapter_generate(chapter_context)
    assert chapter_blueprint.title in "\n".join(chapter_fake_llm.structured_prompts[1])
    assert chapter_fake_llm.structured_output_requests == snapshot(
        [
            {
                "schema": ChapterBlueprint,
                "include_raw": False,
                "method": "function_calling",
                "strict": True,
            },
            {
                "schema": ChapterScene,
                "include_raw": False,
                "method": "function_calling",
                "strict": True,
            },
        ]
    )

    assert chapter == chapter_outline
