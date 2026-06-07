import pytest

from app.api.app import create_app
from app.api.routes.outline import get_bible, get_substory
from app.modules.outlines.schemas import Bible, Substory


class FakeOutlineOrchestrator:
    def __init__(self, *, bible: Bible, substory: Substory) -> None:
        self.bible = bible
        self.substory = substory
        self.requested_bible_id: str | None = None
        self.requested_substory_id: str | None = None

    async def get_bible(self, *, bible_id: str) -> Bible:
        self.requested_bible_id = bible_id
        return self.bible

    async def get_substory(self, *, substory_id: str) -> Substory:
        self.requested_substory_id = substory_id
        return self.substory


@pytest.mark.asyncio()
async def test_get_bible_returns_bible_response(bible: Bible, substory: Substory) -> None:
    orchestrator = FakeOutlineOrchestrator(bible=bible, substory=substory)

    response = await get_bible("bible_1", orchestrator)

    assert response.bible == bible
    assert orchestrator.requested_bible_id == "bible_1"


@pytest.mark.asyncio()
async def test_get_substory_returns_substory_response(bible: Bible, substory: Substory) -> None:
    orchestrator = FakeOutlineOrchestrator(bible=bible, substory=substory)

    response = await get_substory("substory_1", orchestrator)

    assert response.substory == substory
    assert orchestrator.requested_substory_id == "substory_1"


def test_outline_openapi_includes_detail_paths() -> None:
    schema = create_app().openapi()

    assert "/outline/bible/{bible_id}" in schema["paths"]
    assert "/outline/substory/{substory_id}" in schema["paths"]
