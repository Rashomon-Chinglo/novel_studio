from collections.abc import Callable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.persistence.db import SessionFactory
from app.persistence.repositories.groups import (
    MaterialsRepositoryGroup,
    OutlinesRepositoryGroup,
    PostWritingRepositoryGroup,
    WorkflowRepositoryGroup,
    WritingRepositoryGroup,
    build_repository_groups,
)


class SqlAlchemyUnitOfWork:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] | Callable[[], AsyncSession] = (
            SessionFactory
        ),
    ) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None
        self.outlines: OutlinesRepositoryGroup | None = None
        self.materials: MaterialsRepositoryGroup | None = None
        self.post_writing: PostWritingRepositoryGroup | None = None
        self.workflow: WorkflowRepositoryGroup | None = None
        self.writing: WritingRepositoryGroup | None = None

    def _clear_state(self) -> None:
        self._session = None
        self.outlines = None
        self.materials = None
        self.post_writing = None
        self.workflow = None
        self.writing = None

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError("UnitOfWork session has not been started.")
        return self._session

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self._session = self._session_factory()
        repository_groups = build_repository_groups(self.session)
        self.outlines = repository_groups.outlines
        self.materials = repository_groups.materials
        self.post_writing = repository_groups.post_writing
        self.workflow = repository_groups.workflow
        self.writing = repository_groups.writing
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
