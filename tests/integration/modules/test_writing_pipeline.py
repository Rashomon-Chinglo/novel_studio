import pytest
from inline_snapshot import snapshot
from pytest_mock import MockerFixture

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.outlines.schemas import Bible, Substory
from app.modules.outlines.schemas.chapter import Chapter as ChapterOutline
from app.modules.outlines.schemas.chapter import ChapterBlueprint
from app.modules.outlines.schemas.substory import ChapterOriginalSubstoryNodes
from app.modules.writing.context import ChapterWritingContext
from app.modules.writing.engine import WritingEngine
from app.modules.writing.providers import MaterialProvider
from app.modules.writing.schemas import Chapter


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
        chapter=chapter_outline,
        chapter_blueprint=chapter_blueprint,
        cumulative_substory_summary=cumulative_substory_summary,
        pre_chapter_summary=chapter_summary,
        previous_content="李四站在门前，犹豫了片刻。",
        original_logic_nodes=chapter_original_substory_nodes,
    )


@pytest.fixture()
def writing_engine(material_provider: MaterialProvider, mocker: MockerFixture) -> WritingEngine:
    scene_writing_chain = mocker.patch("app.modules.writing.engine.get_scene_writing_chain")
    scene_writing_chain.return_value.ainvoke = mocker.AsyncMock(return_value="测试文本")
    return WritingEngine(material_provider=material_provider)


@pytest.mark.integration()
@pytest.mark.asyncio()
async def test_writing_pipeline(
    writing_engine: WritingEngine,
    chapter_writing_context: ChapterWritingContext,
) -> None:
    result = await writing_engine.writing(chapter_writing_context)
    assert isinstance(result, Chapter)
    assert len(result.chunks) == snapshot(1)
    assert result.chunks[0].content == snapshot("测试文本")
