from app.modules.outlines.chain.bible import get_bible_chain
from app.modules.outlines.chain.bible import get_brainstorm_chain
from app.modules.outlines.prompts.bible import BibleBrainstormPrompt, BibleGeneratePrompt
import pytest
from inline_snapshot import snapshot
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers.openai_tools import PydanticToolsParser


@pytest.fixture()
def bible_prompt() -> BibleBrainstormPrompt:
    return BibleBrainstormPrompt()


@pytest.fixture()
def bible_generate_prompt() -> BibleGeneratePrompt:
    return BibleGeneratePrompt()


@pytest.mark.unit()
def test_get_brainstorm_chain(bible_prompt: BibleBrainstormPrompt):
    chain = get_brainstorm_chain(bible_prompt.prompt)

    assert isinstance(chain, RunnableSequence)
    assert [type(step).__name__ for step in chain.steps] == snapshot(
        ["ChatPromptTemplate", "ChatOpenAI", "StrOutputParser"]
    )


@pytest.mark.unit()
def test_get_generate_chain(bible_generate_prompt: BibleGeneratePrompt):
    chain = get_bible_chain(bible_generate_prompt.prompt)

    assert isinstance(chain, RunnableSequence)
    assert [type(step).__name__ for step in chain.steps] == snapshot(
        ["ChatPromptTemplate", "RunnableBinding", "PydanticToolsParser"]
    )
    assert isinstance(chain.steps[-1], PydanticToolsParser)
    assert [tool.__name__ for tool in chain.steps[-1].tools] == snapshot(["Bible"])
