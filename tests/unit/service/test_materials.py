from types import SimpleNamespace

import pytest

from app.modules.materials.schemas import MaterialSnippet
from app.service.materials import MaterialService


class FakeSnippetRepository:
    def __init__(self) -> None:
        self.saved = []

    def add_many(self, snippets) -> None:
        self.saved.extend(snippets)


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.materials = SimpleNamespace(snippets=FakeSnippetRepository())
        self.committed = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None

    async def commit(self) -> None:
        self.committed = True


class FakeVectorStore:
    def __init__(self) -> None:
        self.payload = None

    def add_texts(self, **kwargs) -> None:
        self.payload = kwargs

    async def aadd_texts(self, **kwargs) -> None:
        self.payload = kwargs


@pytest.mark.asyncio()
async def test_save_snippets_uses_uow_and_vector_store() -> None:
    created_uows: list[FakeUnitOfWork] = []

    def uow_factory() -> FakeUnitOfWork:
        uow = FakeUnitOfWork()
        created_uows.append(uow)
        return uow

    vector_store = FakeVectorStore()
    service = MaterialService(vector_store=vector_store, uow_factory=uow_factory)
    snippets = [
        MaterialSnippet(
            essential_text="阴暗的走廊里弥漫着铁锈的味道。",
            category="环境",
            mood="压抑",
            tags=["环境描写", "氛围感"],
        )
    ]

    await service.save_snippets("测试标题", snippets)

    assert len(created_uows) == 1
    assert created_uows[0].committed is True
    assert len(created_uows[0].materials.snippets.saved) == 1
    assert created_uows[0].materials.snippets.saved[0].title == "测试标题"
    assert vector_store.payload is not None
    assert vector_store.payload["metadatas"][0]["title"] == "测试标题"
