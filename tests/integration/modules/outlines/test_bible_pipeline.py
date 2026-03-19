import pytest
from app.modules.outlines.schemas import Bible
from app.modules.outlines.engines.bible import BibleEngine


@pytest.fixture()
def bible_brainstorm_context() -> BibleEngine.BibleBrainstormContext:
    return BibleEngine.BibleBrainstormContext(history=[], user_input="这个主意就挺好的")


@pytest.mark.integration()
@pytest.mark.asyncio()
async def test_bible_pipeline(
    bible_engine: BibleEngine,
    bible_brainstorm_context: BibleEngine.BibleBrainstormContext,
    bible: Bible,
) -> None:
    messages = [*bible_brainstorm_context.history, bible_brainstorm_context.user_input]
    result = await bible_engine.brainstorm(bible_brainstorm_context)
    messages = [*messages, result]
    bible_generate_context = BibleEngine.BibleGenerateContext(messages=messages)
    result = await bible_engine.generate(bible_generate_context)
    assert result == bible
