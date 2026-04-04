from collections.abc import Callable

from app.core import utc_now
from app.domain import WorkflowErrorCode, WorkflowStage, WorkflowStatus, WorkflowType
from app.persistence import SqlAlchemyUnitOfWork
from app.persistence.models import WorkflowRun


class WorkflowRunService:
    def __init__(
        self, uow_factory: Callable[[], SqlAlchemyUnitOfWork] = SqlAlchemyUnitOfWork
    ) -> None:
        self.uow_factory: Callable[[], SqlAlchemyUnitOfWork] = uow_factory

    async def create(
        self,
        *,
        bible_id: str,
        substory_id: str,
        chapter_outline_id: str,
        chapter_index: int,
    ) -> WorkflowRun:
        async with self.uow_factory() as uow:
            run = WorkflowRun(
                workflow_type=WorkflowType.CHAPTER_GENERATION,
                status=WorkflowStatus.PENDING,
                current_stage=WorkflowStage.LOAD_CONTEXT,
                bible_id=bible_id,
                substory_id=substory_id,
                chapter_outline_id=chapter_outline_id,
                chapter_index=chapter_index,
            )
            uow.workflow.workflow_runs.add(run)
            await uow.commit()
            return run

    async def mark_stage(self, run_id: str, stage: WorkflowStage):
        async with self.uow_factory() as uow:
            run = await uow.workflow.workflow_runs.get(run_id)
            if run is None:
                raise ValueError(f"Workflow run {run_id} not found.")
            match run.status:
                case WorkflowStatus.SUCCEEDED | WorkflowStatus.FAILED:
                    raise ValueError(f"Workflow run {run_id} is already finished.")
                case WorkflowStatus.PENDING:
                    run.status = WorkflowStatus.RUNNING
                case WorkflowStatus.RUNNING:
                    pass
            run.current_stage = stage
            await uow.commit()

    async def mark_failed(self, run_id: str, error_code: WorkflowErrorCode, error_message: str):
        async with self.uow_factory() as uow:
            run = await uow.workflow.workflow_runs.get(run_id)
            if run is None:
                raise ValueError(f"Workflow run {run_id} not found.")
            match run.status:
                case WorkflowStatus.SUCCEEDED | WorkflowStatus.FAILED:
                    raise ValueError(f"Workflow run {run_id} is already finished.")
                case WorkflowStatus.PENDING | WorkflowStatus.RUNNING:
                    run.status = WorkflowStatus.FAILED
                    run.error_code = error_code
                    run.error_message = error_message
                    run.finished_at = utc_now()
            await uow.commit()

    async def mark_succeeded(self, run_id: str):
        async with self.uow_factory() as uow:
            run = await uow.workflow.workflow_runs.get(run_id)
            if run is None:
                raise ValueError(f"Workflow run {run_id} not found.")
            match run.status:
                case WorkflowStatus.SUCCEEDED | WorkflowStatus.FAILED:
                    raise ValueError(f"Workflow run {run_id} is already finished.")
                case WorkflowStatus.PENDING | WorkflowStatus.RUNNING:
                    run.status = WorkflowStatus.SUCCEEDED
                    run.finished_at = utc_now()
            await uow.commit()

    async def get(self, run_id: str) -> WorkflowRun | None:
        async with self.uow_factory() as uow:
            return await uow.workflow.workflow_runs.get(run_id)
