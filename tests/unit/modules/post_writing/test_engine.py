import pytest
from inline_snapshot import snapshot
from pytest_mock import MockerFixture

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.post_writing.context import ChapterSummaryContext, SubstoryCumulativeSummaryContext
from app.modules.post_writing.engine import PostWritingEngine
from tests.support.llm import EngineContext, FakeLLMFactory


@pytest.fixture()
def chapter_summary_engine_context(
    mocker: MockerFixture, fake_llm_factory: FakeLLMFactory
) -> EngineContext[PostWritingEngine, None]:
    fake_llm = fake_llm_factory(text_responses=["测试章节总结"])
    mocker.patch("app.modules.post_writing.chain.get_llm", return_value=fake_llm)
    return EngineContext(engine=PostWritingEngine(), fake_llm=fake_llm)


@pytest.fixture()
def cumulative_summary_engine_context(
    mocker: MockerFixture, fake_llm_factory: FakeLLMFactory
) -> EngineContext[PostWritingEngine, None]:
    fake_llm = fake_llm_factory(text_responses=["测试累积总结"])
    mocker.patch("app.modules.post_writing.chain.get_llm", return_value=fake_llm)
    return EngineContext(engine=PostWritingEngine(), fake_llm=fake_llm)


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_post_writing_engine_chapter_summary(
    chapter_summary_engine_context: EngineContext[PostWritingEngine, str],
    chapter_summary_context: ChapterSummaryContext,
) -> None:
    engine = chapter_summary_engine_context.engine
    fake_llm = chapter_summary_engine_context.fake_llm
    result = await engine.chapter_summary(chapter_summary_context)

    assert result == snapshot(ChapterSummary(summary="测试章节总结"))
    assert chapter_summary_context.cumulative_substory_summary.summary in "\n".join(
        fake_llm.plain_prompts[0]
    )


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_post_writing_engine_cumulative_substory_summary(
    cumulative_summary_engine_context: EngineContext[PostWritingEngine, str],
    substory_cumulative_summary_context: SubstoryCumulativeSummaryContext,
) -> None:
    engine = cumulative_summary_engine_context.engine
    fake_llm = cumulative_summary_engine_context.fake_llm
    result = await engine.cumulative_substory_summary(substory_cumulative_summary_context)

    assert result == snapshot(CumulativeSubstorySummary(summary="测试累积总结"))
    assert substory_cumulative_summary_context.cumulative_substory_summary.summary in "\n".join(
        fake_llm.plain_prompts[0]
    )
