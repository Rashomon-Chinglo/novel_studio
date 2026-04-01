from importlib import import_module
from types import ModuleType
from typing import TYPE_CHECKING, Any

__all__ = [
    "AsyncSessionLocal",
    "Base",
    "BibleRepository",
    "ChapterOutlineRepository",
    "SnippetRepository",
    "SqlAlchemyUnitOfWork",
    "SubstoryRepository",
    "WorkflowRunRepository",
    "get_vector_store",
    "init_sqlite_db",
    "models",
]

_EXPORTS: dict[str, tuple[str, str] | ModuleType] = {
    "AsyncSessionLocal": (".db", "AsyncSessionLocal"),
    "Base": (".db", "Base"),
    "BibleRepository": (".repositories", "BibleRepository"),
    "ChapterOutlineRepository": (".repositories", "ChapterOutlineRepository"),
    "SnippetRepository": (".repositories", "SnippetRepository"),
    "SqlAlchemyUnitOfWork": (".db.unit_of_work", "SqlAlchemyUnitOfWork"),
    "SubstoryRepository": (".repositories", "SubstoryRepository"),
    "WorkflowRunRepository": (".repositories", "WorkflowRunRepository"),
    "get_vector_store": (".db", "get_vector_store"),
    "init_sqlite_db": (".db", "init_sqlite_db"),
}

if TYPE_CHECKING:
    from . import models
    from .db import AsyncSessionLocal, Base, get_vector_store, init_sqlite_db
    from .db.unit_of_work import SqlAlchemyUnitOfWork
    from .repositories import (
        BibleRepository,
        ChapterOutlineRepository,
        SnippetRepository,
        SubstoryRepository,
        WorkflowRunRepository,
    )


def __getattr__(name: str) -> Any:
    if name == "models":
        module = import_module(".models", __name__)
        globals()[name] = module
        return module

    try:
        module_name, attr_name = _EXPORTS[name]  # type: ignore[misc]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
