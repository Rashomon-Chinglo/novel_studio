import pytest
from inline_snapshot import snapshot

from app.modules.outlines.engines.substory import SubstoryEngine
from app.modules.outlines.schemas import Bible, Substory
from tests.support.llm import EngineContext


@pytest.fixture()
def substory_brainstorm_context(bible: Bible) -> SubstoryEngine.SubstoryBrainstormContext:
    return SubstoryEngine.SubstoryBrainstormContext(
        history=[], user_input="这个主意就挺好的", bible=bible
    )


@pytest.mark.integration()
@pytest.mark.asyncio()
async def test_substory_pipeline(
    substory_engine_context: EngineContext[SubstoryEngine, Substory],
    substory_brainstorm_context: SubstoryEngine.SubstoryBrainstormContext,
    substory: Substory,
) -> None:
    substory_engine = substory_engine_context.engine
    fake_llm = substory_engine_context.fake_llm
    messages = [*substory_brainstorm_context.history, substory_brainstorm_context.user_input]
    brainstorm_result = await substory_engine.brainstorm(substory_brainstorm_context)
    messages = [*messages, brainstorm_result]
    substory_generate_context = SubstoryEngine.SubstoryGenerateContext(
        messages=messages, bible=substory_brainstorm_context.bible
    )
    result = await substory_engine.generate(substory_generate_context)
    assert result == substory
    assert substory_brainstorm_context.user_input in "\n".join(fake_llm.plain_prompts[0])
    assert brainstorm_result in "\n".join(fake_llm.structured_prompts[0])
    assert fake_llm.structured_output_requests == snapshot(
        [{"schema": Substory, "include_raw": False, "method": "function_calling", "strict": True}]
    )
