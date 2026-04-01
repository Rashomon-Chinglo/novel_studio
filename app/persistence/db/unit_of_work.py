from collections.abc import Callable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.persistence.db.session import AsyncSessionLocal
from app.persistence.repositories.materials import SnippetRepository
from app.persistence.repositories.outlines import (
    BibleRepository,
    ChapterOutlineRepository,
    SubstoryRepository,
)


class OutlinesRepositoryGroup:
    def __init__(self, session: AsyncSession) -> None:
        self.bibles = BibleRepository(session)
        self.substories = SubstoryRepository(session)
        self.chapter_outlines = ChapterOutlineRepository(session)


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
        self._session: AsyncSession | None = None
        self.outlines: OutlinesRepositoryGroup | None = None
        self.materials: MaterialsRepositoryGroup | None = None

    def _clear_state(self) -> None:
        self._session = None
        self.outlines = None
        self.materials = None

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError("UnitOfWork session has not been started.")
        return self._session

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self._session = self._session_factory()
        self.outlines = OutlinesRepositoryGroup(self.session)
        self.materials = MaterialsRepositoryGroup(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._session is None:
            return
        try:
            if exc is not None:
                await self.rollback()
            await self._session.close()
        finally:
            self._clear_state()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
