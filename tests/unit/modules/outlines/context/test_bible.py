from app.modules.outlines.context.bible import BibleBrainstormContext
from app.modules.outlines.context.bible import BibleGenerateContext
from inline_snapshot import snapshot
import pytest


@pytest.mark.unit()
def test_bible_brainstorm_context(
    history: list[str],
    user_input: str,
):
    context = BibleBrainstormContext(
        history=history,
        user_input=user_input,
    )
    assert context.model_dump() == snapshot({"history": ["test", "history"], "user_input": "test"})


@pytest.mark.unit()
def test_bible_generate_context(
    messages: list[str],
):
    context = BibleGenerateContext(
        messages=messages,
    )
    assert context.model_dump() == snapshot({"messages": ["test", "messages"]})
