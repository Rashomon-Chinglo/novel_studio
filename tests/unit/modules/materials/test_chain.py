from app.modules.materials.chain import get_mining_chain
from app.modules.materials.prompt import MaterialsMiningPrompt
import pytest
from inline_snapshot import snapshot
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers.openai_tools import PydanticToolsParser


@pytest.fixture()
def materials_prompt() -> MaterialsMiningPrompt:
    return MaterialsMiningPrompt()


@pytest.mark.unit()
def test_get_mining_chain(materials_prompt: MaterialsMiningPrompt) -> None:
    chain = get_mining_chain(materials_prompt.prompt)
    assert isinstance(chain, RunnableSequence)
    assert [type(step).__name__ for step in chain.steps] == snapshot(
        ["ChatPromptTemplate", "RunnableBinding", "PydanticToolsParser"]
    )
    assert isinstance(chain.steps[-1], PydanticToolsParser)
    assert [tool.__name__ for tool in chain.steps[-1].tools] == snapshot(["ExtractedResult"])
