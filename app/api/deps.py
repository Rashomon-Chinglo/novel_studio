"""Dependency providers for API routes."""

from functools import lru_cache

from app.orchestrator.chapter import ChapterOrchestrator
from app.orchestrator.outline import OutlineOrchestrator
from app.service.materials import MaterialService


@lru_cache
def get_outline_orchestrator() -> OutlineOrchestrator:
    return OutlineOrchestrator()


@lru_cache
def get_material_service() -> MaterialService:
    return MaterialService()


@lru_cache
def get_chapter_orchestrator() -> ChapterOrchestrator:
    return ChapterOrchestrator()
