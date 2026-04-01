from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "Bible",
    "ChapterBlueprint",
    "ChapterOutline",
    "ChapterSummary",
    "CumulativeSubstorySummary",
    "Snippet",
    "Substory",
    "WorkflowRun",
    "WrittenChapter",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "Bible": (".outline", "Bible"),
    "ChapterBlueprint": (".outline", "ChapterBlueprint"),
    "ChapterOutline": (".outline", "ChapterOutline"),
    "ChapterSummary": (".post_writing", "ChapterSummary"),
    "CumulativeSubstorySummary": (".post_writing", "CumulativeSubstorySummary"),
    "Snippet": (".snippet", "Snippet"),
    "Substory": (".outline", "Substory"),
    "WorkflowRun": (".workflow", "WorkflowRun"),
    "WrittenChapter": (".writing", "WrittenChapter"),
}

if TYPE_CHECKING:
    from .outline import Bible, ChapterBlueprint, ChapterOutline, Substory
    from .post_writing import ChapterSummary, CumulativeSubstorySummary
    from .snippet import Snippet
    from .workflow import WorkflowRun
    from .writing import WrittenChapter


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
