import pytest
from inline_snapshot import snapshot

from app.modules.outlines.prompts.bible import BibleBrainstormPrompt
from app.modules.outlines.prompts.bible import BibleGeneratePrompt
from app.modules.outlines.context.bible import BibleBrainstormContext
from app.modules.outlines.context.bible import BibleGenerateContext
from langchain_core.prompts import ChatPromptTemplate


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
test
history\
""",
            "user_input": "test",
        }
    )


@pytest.mark.unit()
def test_bible_brainstorm_prompt_prompt(bible_brainstorm_prompt: BibleBrainstormPrompt) -> None:
    assert isinstance(bible_brainstorm_prompt.prompt, ChatPromptTemplate)


@pytest.mark.unit()
def test_bible_brainstorm_prompt_version(bible_brainstorm_prompt: BibleBrainstormPrompt) -> None:
    assert bible_brainstorm_prompt.version() == snapshot("1.0.0")


@pytest.mark.unit()
def test_bible_generate_prompt_template(bible_generate_prompt: BibleGeneratePrompt) -> None:
    assert len(bible_generate_prompt.template) == snapshot(737)


@pytest.mark.unit()
def test_bible_generate_prompt_build_variables(
    bible_generate_prompt: BibleGeneratePrompt, bible_generate_context: BibleGenerateContext
):
    assert bible_generate_prompt.build_variables(bible_generate_context) == snapshot(
        {
            "conversation_text": """\
test
messages\
"""
        }
    )


@pytest.mark.unit()
def test_bible_generate_prompt_prompt(bible_generate_prompt: BibleGeneratePrompt) -> None:
    assert isinstance(bible_generate_prompt.prompt, ChatPromptTemplate)


@pytest.mark.unit()
def test_bible_generate_prompt_version(bible_generate_prompt: BibleGeneratePrompt) -> None:
    assert bible_generate_prompt.version() == snapshot("1.0.0")
