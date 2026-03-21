import pytest
from inline_snapshot import snapshot

from app.modules.outlines.engines.bible import BibleEngine
from app.modules.outlines.schemas import Bible
from tests.support.llm import EngineContext


@pytest.fixture()
def bible_brainstorm_context() -> BibleEngine.BibleBrainstormContext:
    return BibleEngine.BibleBrainstormContext(history=[], user_input="这个主意就挺好的")


@pytest.mark.integration()
@pytest.mark.asyncio()
async def test_bible_pipeline(
    bible_engine_context: EngineContext[BibleEngine, Bible],
    bible_brainstorm_context: BibleEngine.BibleBrainstormContext,
    bible: Bible,
) -> None:
    bible_engine = bible_engine_context.engine
    fake_llm = bible_engine_context.fake_llm
    messages = [*bible_brainstorm_context.history, bible_brainstorm_context.user_input]
    brainstorm_result = await bible_engine.brainstorm(bible_brainstorm_context)
    messages = [*messages, brainstorm_result]
    bible_generate_context = BibleEngine.BibleGenerateContext(messages=messages)
    result = await bible_engine.generate(bible_generate_context)
    assert bible_brainstorm_context.user_input in "\n".join(fake_llm.plain_prompts[0])
    assert brainstorm_result in "\n".join(fake_llm.structured_prompts[0])
    assert result == bible
    assert fake_llm.structured_output_requests == snapshot(
        [{"schema": Bible, "include_raw": False, "method": "function_calling", "strict": True}]
    )
