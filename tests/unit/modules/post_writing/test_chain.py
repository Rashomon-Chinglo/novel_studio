import pytest
from inline_snapshot import snapshot
from langchain_core.runnables import RunnableSequence

from app.modules.post_writing.chain import (
    get_chapter_summary_chain,
    get_cumulative_substory_summary_chain,
)
from app.modules.post_writing.prompt import ChapterSummaryPrompt, SubstoryCumulativeSummaryPrompt


@pytest.fixture()
def chapter_summary_prompt() -> ChapterSummaryPrompt:
    return ChapterSummaryPrompt()


@pytest.fixture()
def substory_cumulative_summary_prompt() -> SubstoryCumulativeSummaryPrompt:
    return SubstoryCumulativeSummaryPrompt()


@pytest.mark.unit()
def test_get_chapter_summary_chain(chapter_summary_prompt: ChapterSummaryPrompt) -> None:
    chain = get_chapter_summary_chain(chapter_summary_prompt.prompt)

    assert isinstance(chain, RunnableSequence)
    assert [type(step).__name__ for step in chain.steps] == snapshot(
        ["ChatPromptTemplate", "ChatOpenAI", "StrOutputParser"]
    )


@pytest.mark.unit()
def test_get_cumulative_substory_summary_chain(
    substory_cumulative_summary_prompt: SubstoryCumulativeSummaryPrompt,
) -> None:
    chain = get_cumulative_substory_summary_chain(substory_cumulative_summary_prompt.prompt)

    assert isinstance(chain, RunnableSequence)
    assert [type(step).__name__ for step in chain.steps] == snapshot(
        ["ChatPromptTemplate", "ChatOpenAI", "StrOutputParser"]
    )
