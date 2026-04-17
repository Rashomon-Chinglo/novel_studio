"""Chapter API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_chapter_orchestrator
from app.api.schemas.chapter import (
    ChapterRunStatusResponse,
    StartChapterRequest,
    StartChapterResponse,
)
from app.orchestrator.chapter import ChapterOrchestrator

router = APIRouter(prefix="/chapters", tags=["chapters"])


@router.post("", response_model=StartChapterResponse)
async def start_chapter(
    request: StartChapterRequest,
    orchestrator: Annotated[ChapterOrchestrator, Depends(get_chapter_orchestrator)],
) -> StartChapterResponse:
    workflow_run_id = await orchestrator.start(
        bible_id=request.bible_id,
        substory_id=request.substory_id,
        chapter_index=request.chapter_index,
        substory_chapter_index=request.substory_chapter_index,
    )
    return StartChapterResponse(workflow_run_id=workflow_run_id)


@router.get("/runs/{run_id}", response_model=ChapterRunStatusResponse)
async def get_chapter_run_status(
    run_id: str,
    orchestrator: Annotated[ChapterOrchestrator, Depends(get_chapter_orchestrator)],
) -> ChapterRunStatusResponse:
    status = await orchestrator.get_status(run_id)
    return ChapterRunStatusResponse(
        id=status.id,
        status=status.status,
        current_stage=status.current_stage,
        bible_id=status.bible_id,
        substory_id=status.substory_id,
        chapter_index=status.chapter_index,
        substory_chapter_index=status.substory_chapter_index,
        error_code=status.error_code,
        error_message=status.error_message,
        started_at=status.started_at,
        finished_at=status.finished_at,
    )
