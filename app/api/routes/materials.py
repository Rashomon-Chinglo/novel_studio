"""Materials API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_material_service
from app.api.schemas.materials import (
    LexicalSearchMaterialsRequest,
    MaterialsSearchResponse,
    MineMaterialsRequest,
    MineMaterialsResponse,
    SemanticSearchMaterialsRequest,
)
from app.service.materials import MaterialService

router = APIRouter(prefix="/materials", tags=["materials"])


@router.post("/mine", response_model=MineMaterialsResponse)
async def mine_materials(
    request: MineMaterialsRequest,
    material_service: Annotated[MaterialService, Depends(get_material_service)],
) -> MineMaterialsResponse:
    created_snippet_count = await material_service.mine_content(request.full_text)
    return MineMaterialsResponse(created_snippet_count=created_snippet_count)


@router.post("/search/semantic", response_model=MaterialsSearchResponse)
async def search_materials_semantic(
    request: SemanticSearchMaterialsRequest,
    material_service: Annotated[MaterialService, Depends(get_material_service)],
) -> MaterialsSearchResponse:
    snippets = await material_service.search_semantic(
        query=request.query,
        limit=request.limit,
        category=request.category,
        mood=request.mood,
    )
    return MaterialsSearchResponse(snippets=snippets)


@router.post("/search/lexical", response_model=MaterialsSearchResponse)
async def search_materials_lexical(
    request: LexicalSearchMaterialsRequest,
    material_service: Annotated[MaterialService, Depends(get_material_service)],
) -> MaterialsSearchResponse:
    snippets = await material_service.search_lexical(
        query=request.query,
        limit=request.limit,
        category=request.category,
        mood=request.mood,
        tags=request.tags,
    )
    return MaterialsSearchResponse(snippets=snippets)
