import pytest
from inline_snapshot import snapshot
from pytest_mock import MockerFixture

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.outlines.schemas.bible import Bible
from app.modules.outlines.schemas.chapter import ChapterOutline
from app.modules.outlines.schemas.substory import ChapterOriginalSubstoryNodes, Substory
from app.modules.post_writing.engine import PostWritingEngine
from app.modules.writing.schemas import SceneChunk, WrittenChapter
from tests.support.llm import EngineContext, FakeLLM, FakeLLMFactory


@pytest.fixture()
def written_chapter() -> WrittenChapter:
    return WrittenChapter(
        chunks=[
            SceneChunk(content="第一场戏内容。"),
            SceneChunk(content="第二场戏内容。"),
        ]
    )


@pytest.fixture()
def post_writing_engine_context(
    mocker: MockerFixture, fake_llm_factory: FakeLLMFactory
) -> EngineContext[PostWritingEngine, str]:
    fake_llm: FakeLLM[str] = fake_llm_factory(
        text_responses=["这是本章的剧情梗概", "这是本卷的累计剧情梗概"],
    )
    mocker.patch("app.modules.post_writing.chain.get_llm", return_value=fake_llm)
    return EngineContext(engine=PostWritingEngine(), fake_llm=fake_llm)


@pytest.mark.integration()
@pytest.mark.asyncio()
async def test_post_writing_pipeline(
    post_writing_engine_context: EngineContext[PostWritingEngine, str],
    cumulative_substory_summary: CumulativeSubstorySummary,
    chapter_summary: ChapterSummary,
    bible: Bible,
    substory: Substory,
    chapter_original_substory_nodes: ChapterOriginalSubstoryNodes,
    chapter_outline: ChapterOutline,
    written_chapter: WrittenChapter,
) -> None:
    post_writing_engine = post_writing_engine_context.engine
    fake_llm = post_writing_engine_context.fake_llm

    current_chapter_summary = await post_writing_engine.chapter_summary(
        post_writing_engine.ChapterSummaryContext(
            bible=bible,
            substory=substory,
            original_logic_nodes=chapter_original_substory_nodes,
            chapter_outline=chapter_outline,
            cumulative_substory_summary=cumulative_substory_summary,
            pre_chapter_summary=chapter_summary,
            written_chapter=written_chapter,
        )
    )

    assert current_chapter_summary.summary == snapshot("这是本章的剧情梗概")
    assert cumulative_substory_summary.summary in "\n".join(fake_llm.plain_prompts[0])
    assert chapter_summary.summary in "\n".join(fake_llm.plain_prompts[0])
    assert fake_llm.structured_output_requests == snapshot([])

    cumulative_substory_summary = await post_writing_engine.cumulative_substory_summary(
        post_writing_engine.SubstoryCumulativeSummaryContext(
            bible=bible,
            substory=substory,
            cumulative_substory_summary=cumulative_substory_summary,
            current_chapter_summary=current_chapter_summary,
        )
    )

    assert current_chapter_summary.summary in "\n".join(fake_llm.plain_prompts[1])
    assert cumulative_substory_summary.summary == snapshot("这是本卷的累计剧情梗概")
