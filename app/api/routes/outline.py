"""Outline API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_outline_orchestrator
from app.api.schemas.outline import (
    BibleResponse,
    BrainstormBibleRequest,
    BrainstormResponse,
    BrainstormSubstoryRequest,
    CreateBibleRequest,
    CreateBibleResponse,
    CreateSubstoryRequest,
    CreateSubstoryResponse,
    SubstoryResponse,
)
from app.orchestrator.outline import OutlineOrchestrator

router = APIRouter(prefix="/outline", tags=["outline"])


@router.post("/bible/brainstorm", response_model=BrainstormResponse)
async def brainstorm_bible(
    request: BrainstormBibleRequest,
    orchestrator: Annotated[OutlineOrchestrator, Depends(get_outline_orchestrator)],
) -> BrainstormResponse:
    content = await orchestrator.brainstorm_bible(
        history=request.history,
        user_input=request.user_input,
    )
    return BrainstormResponse(content=content)


@router.post("/bible/create", response_model=CreateBibleResponse)
async def create_bible(
    request: CreateBibleRequest,
    orchestrator: Annotated[OutlineOrchestrator, Depends(get_outline_orchestrator)],
) -> CreateBibleResponse:
    bible_id = await orchestrator.create_bible(messages=request.messages)
    return CreateBibleResponse(bible_id=bible_id)


@router.get("/bible/{bible_id}", response_model=BibleResponse)
async def get_bible(
    bible_id: str,
    orchestrator: Annotated[OutlineOrchestrator, Depends(get_outline_orchestrator)],
) -> BibleResponse:
    bible = await orchestrator.get_bible(bible_id=bible_id)
    return BibleResponse(bible=bible)


@router.post("/substory/brainstorm", response_model=BrainstormResponse)
async def brainstorm_substory(
    request: BrainstormSubstoryRequest,
    orchestrator: Annotated[OutlineOrchestrator, Depends(get_outline_orchestrator)],
) -> BrainstormResponse:
    content = await orchestrator.brainstorm_substory(
        history=request.history,
        user_input=request.user_input,
        bible_id=request.bible_id,
    )
    return BrainstormResponse(content=content)


@router.post("/substory/create", response_model=CreateSubstoryResponse)
async def create_substory(
    request: CreateSubstoryRequest,
    orchestrator: Annotated[OutlineOrchestrator, Depends(get_outline_orchestrator)],
) -> CreateSubstoryResponse:
    substory_id = await orchestrator.create_substory(
        bible_id=request.bible_id,
        substory_order_index=request.substory_order_index,
        messages=request.messages,
    )
    return CreateSubstoryResponse(substory_id=substory_id)


@router.get("/substory/{substory_id}", response_model=SubstoryResponse)
async def get_substory(
    substory_id: str,
    orchestrator: Annotated[OutlineOrchestrator, Depends(get_outline_orchestrator)],
) -> SubstoryResponse:
    substory = await orchestrator.get_substory(substory_id=substory_id)
    return SubstoryResponse(substory=substory)
