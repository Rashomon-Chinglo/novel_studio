import pytest
from inline_snapshot import snapshot
from langchain_core.prompts import ChatPromptTemplate

from app.modules.outlines.context.bible import BibleBrainstormContext, BibleGenerateContext
from app.modules.outlines.prompts.bible import BibleBrainstormPrompt, BibleGeneratePrompt


@pytest.fixture()
def bible_brainstorm_prompt() -> BibleBrainstormPrompt:
    return BibleBrainstormPrompt()


@pytest.fixture()
def bible_generate_prompt() -> BibleGeneratePrompt:
    return BibleGeneratePrompt()


@pytest.mark.unit()
def test_bible_brainstorm_prompt_template(bible_brainstorm_prompt: BibleBrainstormPrompt) -> None:
    assert len(bible_brainstorm_prompt.template) == snapshot(637)


@pytest.mark.unit()
def test_bible_brainstorm_prompt_build_variables(
    bible_brainstorm_prompt: BibleBrainstormPrompt, bible_brainstorm_context: BibleBrainstormContext
) -> None:
    assert bible_brainstorm_prompt.build_variables(bible_brainstorm_context) == snapshot(
        {
            "history": """\
chat_history_1
chat_history_2\
""",
            "user_input": "user_input",
        }
    )


@pytest.mark.unit()
def test_bible_brainstorm_prompt_prompt(bible_brainstorm_prompt: BibleBrainstormPrompt) -> None:
    assert isinstance(bible_brainstorm_prompt.prompt, ChatPromptTemplate)
    assert bible_brainstorm_prompt.prompt.input_variables == snapshot(["history", "user_input"])


@pytest.mark.unit()
def test_bible_brainstorm_prompt_version(bible_brainstorm_prompt: BibleBrainstormPrompt) -> None:
    assert bible_brainstorm_prompt.version() == snapshot("1.0.0")


@pytest.mark.unit()
def test_bible_generate_prompt_template(bible_generate_prompt: BibleGeneratePrompt) -> None:
    assert len(bible_generate_prompt.template) == snapshot(737)


@pytest.mark.unit()
def test_bible_generate_prompt_build_variables(
    bible_generate_prompt: BibleGeneratePrompt, bible_generate_context: BibleGenerateContext
) -> None:
    assert bible_generate_prompt.build_variables(bible_generate_context) == snapshot(
        {
            "conversation_text": """\
chat_history_1
chat_history_2
user_input\
"""
        }
    )


@pytest.mark.unit()
def test_bible_generate_prompt_prompt(bible_generate_prompt: BibleGeneratePrompt) -> None:
    assert isinstance(bible_generate_prompt.prompt, ChatPromptTemplate)
    assert bible_generate_prompt.prompt.input_variables == snapshot(["conversation_text"])


@pytest.mark.unit()
def test_bible_generate_prompt_version(bible_generate_prompt: BibleGeneratePrompt) -> None:
    assert bible_generate_prompt.version() == snapshot("1.0.0")
