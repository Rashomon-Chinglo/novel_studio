"""Chapter API schemas."""

from datetime import datetime

from pydantic import BaseModel

from app.domain import WorkflowErrorCode, WorkflowStage, WorkflowStatus


class StartChapterRequest(BaseModel):
    bible_id: str
    substory_id: str
    chapter_index: int
    substory_chapter_index: int


class StartChapterResponse(BaseModel):
    workflow_run_id: str


class ChapterRunStatusResponse(BaseModel):
    id: str
    status: WorkflowStatus
    current_stage: WorkflowStage
    bible_id: str
    substory_id: str
    chapter_index: int
    substory_chapter_index: int
    error_code: WorkflowErrorCode | None
    error_message: str | None
    started_at: datetime
    finished_at: datetime | None
