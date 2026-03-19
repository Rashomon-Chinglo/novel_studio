import pytest
from inline_snapshot import snapshot

from app.modules.outlines.context.bible import BibleBrainstormContext, BibleGenerateContext


@pytest.mark.unit()
def test_bible_brainstorm_context(
    history: list[str],
    user_input: str,
) -> None:
    context = BibleBrainstormContext(
        history=history,
        user_input=user_input,
    )
    assert context.model_dump() == snapshot(
        {"history": ["chat_history_1", "chat_history_2"], "user_input": "user_input"}
    )


@pytest.mark.unit()
def test_bible_generate_context(
    messages: list[str],
) -> None:
    context = BibleGenerateContext(
        messages=messages,
    )
    assert context.model_dump() == snapshot(
        {"messages": ["chat_history_1", "chat_history_2", "user_input"]}
    )
