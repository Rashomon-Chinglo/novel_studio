from collections.abc import Callable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.persistence.db.session import AsyncSessionLocal
from app.persistence.repositories.materials import SnippetRepository
from app.persistence.repositories.outlines import (
    BibleRepository,
    ChapterRepository,
    SubstoryRepository,
)


class SqlAlchemyUnitOfWork:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] | Callable[[], AsyncSession] = (
            AsyncSessionLocal
        ),
    ) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None
        self.bibles: BibleRepository | None = None
        self.substories: SubstoryRepository | None = None
        self.chapters: ChapterRepository | None = None
        self.snippets: SnippetRepository | None = None

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = self._session_factory()
        self.bibles = BibleRepository(self.session)
        self.substories = SubstoryRepository(self.session)
        self.chapters = ChapterRepository(self.session)
        self.snippets = SnippetRepository(self.session)
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
