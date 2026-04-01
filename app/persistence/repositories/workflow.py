from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models.workflow import WorkflowRun


class WorkflowRunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, workflow_run_id: str) -> WorkflowRun | None:
        return await self.session.get(WorkflowRun, workflow_run_id)

    def add(self, run: WorkflowRun) -> None:
        self.session.add(run)

    async def list_by_bible(self, bible_id: str) -> Sequence[WorkflowRun]:
        result = await self.session.execute(
            select(WorkflowRun)
            .where(WorkflowRun.bible_id == bible_id)
            .order_by(WorkflowRun.started_at.desc())
        )
        return result.scalars().all()

    async def list_by_substory(self, substory_id: str) -> Sequence[WorkflowRun]:
        result = await self.session.execute(
            select(WorkflowRun)
            .where(WorkflowRun.substory_id == substory_id)
            .order_by(WorkflowRun.started_at.desc())
        )
        return result.scalars().all()

    async def list_by_chapter_outline(self, chapter_outline_id: str) -> Sequence[WorkflowRun]:
        result = await self.session.execute(
            select(WorkflowRun)
            .where(WorkflowRun.chapter_outline_id == chapter_outline_id)
            .order_by(WorkflowRun.started_at.desc())
        )
        return result.scalars().all()

    async def get_latest_by_chapter_outline(self, chapter_outline_id: str) -> WorkflowRun | None:
        result = await self.session.execute(
            select(WorkflowRun)
            .where(WorkflowRun.chapter_outline_id == chapter_outline_id)
            .order_by(WorkflowRun.started_at.desc())
            .limit(1)
        )
        return result.scalars().first()
