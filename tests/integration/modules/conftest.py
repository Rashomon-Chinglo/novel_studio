import pytest
from pytest_mock import MockerFixture
from app.modules.outlines.engines.bible import BibleEngine
from app.modules.outlines.schemas import Bible
from app.modules.outlines.engines.substory import SubstoryEngine
from app.modules.outlines.schemas import Substory
from app.modules.outlines.engines.chapter import ChapterEngine
from app.modules.outlines.schemas.chapter import Chapter, ChapterBlueprint, ChapterScene

@pytest.fixture()
def bible_engine(mocker: MockerFixture, bible: Bible) -> BibleEngine:
    brainstorm_chain = mocker.patch("app.modules.outlines.engines.bible.get_brainstorm_chain")
    bible_chain = mocker.patch("app.modules.outlines.engines.bible.get_bible_chain")
    brainstorm_chain.return_value.ainvoke = mocker.AsyncMock(return_value="我认为这是一个好主意")
    bible_chain.return_value.ainvoke = mocker.AsyncMock(return_value=bible)
    return BibleEngine()


@pytest.fixture()
def substory_engine(mocker: MockerFixture, substory: Substory) -> SubstoryEngine:
    brainstorm_chain = mocker.patch("app.modules.outlines.engines.substory.get_brainstorm_chain")
    substory_chain = mocker.patch("app.modules.outlines.engines.substory.get_substory_chain")
    brainstorm_chain.return_value.ainvoke = mocker.AsyncMock(return_value="我认为这是一个好主意")
    substory_chain.return_value.ainvoke = mocker.AsyncMock(return_value=substory)
    return SubstoryEngine()


@pytest.fixture()
def chapter_engine(
    mocker: MockerFixture, chapter_blueprint: ChapterBlueprint, chapter_scene: ChapterScene
) -> ChapterEngine:
    blueprint_chain = mocker.patch(
        "app.modules.outlines.engines.chapter.get_chapter_blueprint_chain"
    )
    blueprint_brainstorm_chain = mocker.patch(
        "app.modules.outlines.engines.chapter.get_chapter_brainstorm_chain"
    )
    scene_chain = mocker.patch("app.modules.outlines.engines.chapter.get_chapter_scene_chain")

    blueprint_chain.return_value.ainvoke = mocker.AsyncMock(return_value=chapter_blueprint)
    blueprint_brainstorm_chain.return_value.ainvoke = mocker.AsyncMock(
        return_value="我认为这是一个好主意"
    )
    scene_chain.return_value.ainvoke = mocker.AsyncMock(return_value=chapter_scene)
    return ChapterEngine()
