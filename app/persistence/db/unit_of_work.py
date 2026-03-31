from collections.abc import Callable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.persistence.db.session import AsyncSessionLocal
from app.persistence.repositories.materials import SnippetRepository
from app.persistence.repositories.outlines import (
    BibleRepository,
    ChapterRepository,
    SubstoryRepository,
)


class OutlinesRepositoryGroup:
    def __init__(self, session: AsyncSession) -> None:
        self.bibles = BibleRepository(session)
        self.substories = SubstoryRepository(session)
        self.chapters = ChapterRepository(session)


class MaterialsRepositoryGroup:
    def __init__(self, session: AsyncSession) -> None:
        self.snippets = SnippetRepository(session)


class SqlAlchemyUnitOfWork:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] | Callable[[], AsyncSession] = (
            AsyncSessionLocal
        ),
    ) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None
        self.outlines: OutlinesRepositoryGroup | None = None
        self.materials: MaterialsRepositoryGroup | None = None

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = self._session_factory()
        self.outlines = OutlinesRepositoryGroup(self.session)
        self.materials = MaterialsRepositoryGroup(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self.session is None:
            return
        if exc is not None:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork session has not been started.")
        await self.session.commit()

    async def rollback(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork session has not been started.")
        await self.session.rollback()
