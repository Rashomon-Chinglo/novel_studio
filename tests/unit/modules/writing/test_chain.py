import pytest
from inline_snapshot import snapshot
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.modules.writing.chain import get_scene_writing_chain
from app.modules.writing.prompt import ChapterSceneWritingPrompt


@pytest.fixture()
def scene_writing_prompt() -> ChapterSceneWritingPrompt:
    return ChapterSceneWritingPrompt()


@pytest.mark.unit()
def test_get_scene_writing_chain(scene_writing_prompt: ChapterSceneWritingPrompt) -> None:
    chain = get_scene_writing_chain(scene_writing_prompt.prompt)

    assert isinstance(chain, RunnableSequence)
    assert len(chain.steps) == snapshot(3)
    assert [type(step).__name__ for step in chain.steps] == snapshot(
        ["ChatPromptTemplate", "ChatOpenAI", "StrOutputParser"]
    )
