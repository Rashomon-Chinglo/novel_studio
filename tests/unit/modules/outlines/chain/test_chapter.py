import pytest
from inline_snapshot import snapshot
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.runnables import RunnableSequence

from app.modules.outlines.chain.chapter import (
    get_chapter_blueprint_chain,
    get_chapter_scene_chain,
)
from app.modules.outlines.prompts.chapter import (
    ChapterBlueprintPrompt,
    ChapterScenePrompt,
)


@pytest.fixture()
def chapter_blueprint_prompt() -> ChapterBlueprintPrompt:
    return ChapterBlueprintPrompt()


@pytest.fixture()
def chapter_scene_prompt() -> ChapterScenePrompt:
    return ChapterScenePrompt()


@pytest.mark.unit()
def test_get_chapter_blueprint_generate_chain(
    chapter_blueprint_prompt: ChapterBlueprintPrompt,
) -> None:
    chain = get_chapter_blueprint_chain(chapter_blueprint_prompt.prompt)

    assert isinstance(chain, RunnableSequence)
    assert [type(step).__name__ for step in chain.steps] == snapshot(
        ["ChatPromptTemplate", "RunnableBinding", "PydanticToolsParser"]
    )
    assert isinstance(chain.steps[-1], PydanticToolsParser)
    assert [tool.__name__ for tool in chain.steps[-1].tools] == snapshot(["ChapterBlueprint"])


@pytest.mark.unit()
def test_get_chapter_scene_generate_chain(chapter_scene_prompt: ChapterScenePrompt) -> None:
    chain = get_chapter_scene_chain(chapter_scene_prompt.prompt)

    assert isinstance(chain, RunnableSequence)
    assert [type(step).__name__ for step in chain.steps] == snapshot(
        ["ChatPromptTemplate", "RunnableBinding", "PydanticToolsParser"]
    )
    assert isinstance(chain.steps[-1], PydanticToolsParser)
    assert [tool.__name__ for tool in chain.steps[-1].tools] == snapshot(["ChapterScene"])
