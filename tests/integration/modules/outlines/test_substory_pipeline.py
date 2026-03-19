import pytest

from app.modules.outlines.engines.substory import SubstoryEngine
from app.modules.outlines.schemas import Bible, Substory


@pytest.fixture()
def substory_brainstorm_context(bible: Bible) -> SubstoryEngine.SubstoryBrainstormContext:
    return SubstoryEngine.SubstoryBrainstormContext(
        history=[], user_input="这个主意就挺好的", bible=bible
    )


@pytest.mark.integration()
@pytest.mark.asyncio()
async def test_substory_pipeline(
    substory_engine: SubstoryEngine,
    substory_brainstorm_context: SubstoryEngine.SubstoryBrainstormContext,
    substory: Substory,
) -> None:
    messages = [*substory_brainstorm_context.history, substory_brainstorm_context.user_input]
    result = await substory_engine.brainstorm(substory_brainstorm_context)
    messages = [*messages, result]
    substory_generate_context = SubstoryEngine.SubstoryGenerateContext(
        messages=messages, bible=substory_brainstorm_context.bible
    )
    result = await substory_engine.generate(substory_generate_context)
    assert result == substory
