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
        self._outlines: OutlinesRepositoryGroup | None = None
        self._materials: MaterialsRepositoryGroup | None = None
        self._post_writing: PostWritingRepositoryGroup | None = None
        self._workflow: WorkflowRepositoryGroup | None = None
        self._writing: WritingRepositoryGroup | None = None

    def _clear_state(self) -> None:
        self._session = None
        self._outlines = None
        self._materials = None
        self._post_writing = None
        self._workflow = None
        self._writing = None

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError("UnitOfWork session has not been started.")
        return self._session

    @property
    def outlines(self) -> OutlinesRepositoryGroup:
        if self._outlines is None:
            raise RuntimeError("Outlines repository group is not available in UnitOfWork.")
        return self._outlines

    @property
    def materials(self) -> MaterialsRepositoryGroup:
        if self._materials is None:
            raise RuntimeError("Materials repository group is not available in UnitOfWork.")
        return self._materials

    @property
    def post_writing(self) -> PostWritingRepositoryGroup:
        if self._post_writing is None:
            raise RuntimeError("Post-writing repository group is not available in UnitOfWork.")
        return self._post_writing

    @property
    def workflow(self) -> WorkflowRepositoryGroup:
        if self._workflow is None:
            raise RuntimeError("Workflow repository group is not available in UnitOfWork.")
        return self._workflow

    @property
    def writing(self) -> WritingRepositoryGroup:
        if self._writing is None:
            raise RuntimeError("Writing repository group is not available in UnitOfWork.")
        return self._writing

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self._session = self._session_factory()
        repository_groups = build_repository_groups(self.session)
        self._outlines = repository_groups.outlines
        self._materials = repository_groups.materials
        self._post_writing = repository_groups.post_writing
        self._workflow = repository_groups.workflow
        self._writing = repository_groups.writing
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
