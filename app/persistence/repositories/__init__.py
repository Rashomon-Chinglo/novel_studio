from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "BibleRepository",
    "ChapterOutlineRepository",
    "ChapterSummaryRepository",
    "CumulativeSubstorySummaryRepository",
    "SnippetRepository",
    "SubstoryRepository",
    "WorkflowRunRepository",
    "WrittenChapterRepository",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "BibleRepository": (".outlines", "BibleRepository"),
    "ChapterOutlineRepository": (".outlines", "ChapterOutlineRepository"),
    "SnippetRepository": (".materials", "SnippetRepository"),
    "SubstoryRepository": (".outlines", "SubstoryRepository"),
    "WorkflowRunRepository": (".workflow", "WorkflowRunRepository"),
    "ChapterSummaryRepository": (".post_writing", "ChapterSummaryRepository"),
    "CumulativeSubstorySummaryRepository": (
        ".post_writing",
        "CumulativeSubstorySummaryRepository",
    ),
    "WrittenChapterRepository": (".writing", "WrittenChapterRepository"),
}

if TYPE_CHECKING:
    from .materials import SnippetRepository
    from .outlines import BibleRepository, ChapterOutlineRepository, SubstoryRepository
    from .post_writing import ChapterSummaryRepository, CumulativeSubstorySummaryRepository
    from .workflow import WorkflowRunRepository
    from .writing import WrittenChapterRepository


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
