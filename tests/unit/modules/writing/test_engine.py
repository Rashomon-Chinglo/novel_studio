import pytest
from inline_snapshot import snapshot
from pytest_mock import MockerFixture

from app.modules.writing.context import ChapterSceneWritingContext, ChapterWritingContext
from app.modules.writing.engine import WritingEngine
from app.modules.writing.providers import MaterialProvider
from app.modules.writing.schemas import SceneChunk, WrittenChapter
from tests.support.llm import EngineContext, FakeLLMFactory


@pytest.fixture()
def scene_writing_engine_context(
    mocker: MockerFixture,
    fake_llm_factory: FakeLLMFactory,
    material_provider: MaterialProvider,
) -> EngineContext[WritingEngine, str]:
    fake_llm = fake_llm_factory(text_responses=["测试场景写作"])
    mocker.patch("app.modules.writing.chain.get_llm", return_value=fake_llm)
    return EngineContext(
        engine=WritingEngine(material_provider=material_provider), fake_llm=fake_llm
    )


@pytest.fixture()
def writing_engine_context(
    mocker: MockerFixture,
    fake_llm_factory: FakeLLMFactory,
    material_provider: MaterialProvider,
) -> EngineContext[WritingEngine, str]:
    fake_llm = fake_llm_factory(text_responses=["第一场戏内容。"])
    mocker.patch("app.modules.writing.chain.get_llm", return_value=fake_llm)
    return EngineContext(
        engine=WritingEngine(material_provider=material_provider), fake_llm=fake_llm
    )


@pytest.mark.asyncio()
@pytest.mark.unit()
async def test_scene_writing(
    scene_writing_engine_context: EngineContext[WritingEngine, str],
    chapter_scene_writing_context: ChapterSceneWritingContext,
) -> None:
    writing_engine = scene_writing_engine_context.engine
    fake_llm = scene_writing_engine_context.fake_llm
    result = await writing_engine.scene_writing(chapter_scene_writing_context)
    assert result == snapshot(SceneChunk(content="测试场景写作"))
    assert chapter_scene_writing_context.scene_blueprint.location in "\n".join(
        fake_llm.plain_prompts[0]
    )


@pytest.mark.asyncio()
@pytest.mark.unit()
async def test_writing(
    writing_engine_context: EngineContext[WritingEngine, str],
    chapter_writing_context: ChapterWritingContext,
    material_provider: MaterialProvider,
) -> None:
    writing_engine = writing_engine_context.engine
    fake_llm = writing_engine_context.fake_llm

    result = await writing_engine.writing(chapter_writing_context)

    assert result == snapshot(WrittenChapter(chunks=[SceneChunk(content="第一场戏内容。")]))
    assert chapter_writing_context.chapter_outline.scenes[0].beats[0].description in "\n".join(
        fake_llm.plain_prompts[0]
    )
