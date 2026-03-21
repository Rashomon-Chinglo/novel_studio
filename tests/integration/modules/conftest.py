import pytest
from pytest_mock import MockerFixture

from app.modules.outlines.engines.bible import BibleEngine
from app.modules.outlines.engines.chapter import ChapterEngine
from app.modules.outlines.engines.substory import SubstoryEngine
from app.modules.outlines.schemas import Bible, Substory
from app.modules.outlines.schemas.chapter import ChapterBlueprint, ChapterScene
from tests.support.llm import EngineContext, FakeLLMFactory


@pytest.fixture()
def bible_engine_context(
    mocker: MockerFixture, bible: Bible, fake_llm_factory: FakeLLMFactory
) -> EngineContext[BibleEngine, Bible]:
    fake_llm = fake_llm_factory(
        text_responses=["我认为这是一个好主意"], structured_responses=[bible]
    )
    mocker.patch("app.modules.outlines.chain.bible.get_llm", return_value=fake_llm)
    return EngineContext(engine=BibleEngine(), fake_llm=fake_llm)


@pytest.fixture()
def substory_engine_context(
    mocker: MockerFixture, substory: Substory, fake_llm_factory: FakeLLMFactory
) -> EngineContext[SubstoryEngine, Substory]:
    fake_llm = fake_llm_factory(
        text_responses=["我认为这是一个好主意"], structured_responses=[substory]
    )
    mocker.patch("app.modules.outlines.chain.substory.get_llm", return_value=fake_llm)
    return EngineContext(engine=SubstoryEngine(), fake_llm=fake_llm)


@pytest.fixture()
def chapter_engine_context(
    mocker: MockerFixture,
    chapter_blueprint: ChapterBlueprint,
    chapter_scene: ChapterScene,
    fake_llm_factory: FakeLLMFactory,
) -> EngineContext[ChapterEngine, ChapterBlueprint | ChapterScene]:
    fake_llm = fake_llm_factory(
        text_responses=["我认为这是一个好主意"],
        structured_responses=[chapter_blueprint, chapter_scene],
    )
    mocker.patch("app.modules.outlines.chain.chapter.get_llm", return_value=fake_llm)
    return EngineContext(engine=ChapterEngine(), fake_llm=fake_llm)
