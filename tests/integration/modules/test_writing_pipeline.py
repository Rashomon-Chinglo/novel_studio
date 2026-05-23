import pytest
from inline_snapshot import snapshot
from pytest_mock import MockerFixture

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.outlines.schemas import Bible, Substory
from app.modules.outlines.schemas.chapter import ChapterBlueprint, ChapterOutline
from app.modules.outlines.schemas.substory import ChapterOriginalSubstoryNodes
from app.modules.writing.context import ChapterWritingContext
from app.modules.writing.engine import WritingEngine
from app.modules.writing.providers import MaterialProvider
from app.modules.writing.schemas import SceneChunk, WrittenChapter
from tests.support.llm import EngineContext, FakeLLM, FakeLLMFactory


@pytest.fixture()
def chapter_writing_context(
    bible: Bible,
    substory: Substory,
    chapter_outline: ChapterOutline,
    chapter_blueprint: ChapterBlueprint,
    chapter_original_substory_nodes: ChapterOriginalSubstoryNodes,
    cumulative_substory_summary: CumulativeSubstorySummary,
    chapter_summary: ChapterSummary,
) -> ChapterWritingContext:
    return ChapterWritingContext(
        bible=bible,
        substory=substory,
        chapter_outline=chapter_outline,
        chapter_blueprint=chapter_blueprint,
        cumulative_substory_summary=cumulative_substory_summary,
        pre_chapter_summary=chapter_summary,
        previous_scene_chunk=SceneChunk(content="李四站在门前，犹豫了片刻。"),
        original_logic_nodes=chapter_original_substory_nodes,
    )


@pytest.fixture()
def writing_engine_context(
    material_provider: MaterialProvider, mocker: MockerFixture, fake_llm_factory: FakeLLMFactory
) -> EngineContext[WritingEngine, WrittenChapter]:
    fake_llm: FakeLLM[WrittenChapter] = fake_llm_factory(text_responses=["测试文本"])
    mocker.patch("app.modules.writing.chain.get_llm", return_value=fake_llm)
    return EngineContext(
        engine=WritingEngine(material_provider=material_provider), fake_llm=fake_llm
    )


@pytest.mark.integration()
@pytest.mark.asyncio()
async def test_writing_pipeline(
    writing_engine_context: EngineContext[WritingEngine, WrittenChapter],
    chapter_writing_context: ChapterWritingContext,
) -> None:
    writing_engine = writing_engine_context.engine
    fake_llm = writing_engine_context.fake_llm
    result = await writing_engine.writing(chapter_writing_context)
    assert isinstance(result, WrittenChapter)
    assert len(result.chunks) == snapshot(1)
    assert result.chunks[0].content == snapshot("测试文本")
    assert chapter_writing_context.cumulative_substory_summary.summary in "\n".join(
        fake_llm.plain_prompts[0]
    )
    assert chapter_writing_context.pre_chapter_summary.summary in "\n".join(
        fake_llm.plain_prompts[0]
    )
    assert chapter_writing_context.previous_scene_chunk.content in "\n".join(
        fake_llm.plain_prompts[0]
    )
