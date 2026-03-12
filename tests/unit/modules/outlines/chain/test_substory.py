import pytest
from inline_snapshot import snapshot
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.runnables import RunnableSequence

from app.modules.outlines.chain.substory import get_brainstorm_chain, get_substory_chain
from app.modules.outlines.prompts.substory import SubstoryBrainstormPrompt, SubstoryGeneratePrompt


@pytest.fixture()
def brainstorm_prompt() -> SubstoryBrainstormPrompt:
    return SubstoryBrainstormPrompt()


@pytest.fixture()
def generate_prompt() -> SubstoryGeneratePrompt:
    return SubstoryGeneratePrompt()


@pytest.mark.unit()
def test_get_brainstorm_chain(brainstorm_prompt: SubstoryBrainstormPrompt) -> None:
    chain = get_brainstorm_chain(brainstorm_prompt.prompt)

    assert isinstance(chain, RunnableSequence)
    assert [type(step).__name__ for step in chain.steps] == snapshot(
        ["ChatPromptTemplate", "ChatOpenAI", "StrOutputParser"]
    )


@pytest.mark.unit()
def test_get_generate_chain(generate_prompt: SubstoryGeneratePrompt) -> None:
    chain = get_substory_chain(generate_prompt.prompt)

    assert isinstance(chain, RunnableSequence)
    assert [type(step).__name__ for step in chain.steps] == snapshot(
        ["ChatPromptTemplate", "RunnableBinding", "PydanticToolsParser"]
    )
    assert isinstance(chain.steps[-1], PydanticToolsParser)
    assert [tool.__name__ for tool in chain.steps[-1].tools] == snapshot(["Substory"])
