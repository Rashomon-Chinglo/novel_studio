from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "BibleRepository",
    "ChapterOutlineRepository",
    "SnippetRepository",
    "SubstoryRepository",
    "WorkflowRunRepository",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "BibleRepository": (".outlines", "BibleRepository"),
    "ChapterOutlineRepository": (".outlines", "ChapterOutlineRepository"),
    "SnippetRepository": (".materials", "SnippetRepository"),
    "SubstoryRepository": (".outlines", "SubstoryRepository"),
    "WorkflowRunRepository": (".workflow", "WorkflowRunRepository"),
}

if TYPE_CHECKING:
    from .materials import SnippetRepository
    from .outlines import BibleRepository, ChapterOutlineRepository, SubstoryRepository
    from .workflow import WorkflowRunRepository


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
