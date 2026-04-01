from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "ChapterSummaryContext",
    "ChapterSummaryPrompt",
    "PostWritingEngine",
    "SubstoryCumulativeSummaryContext",
    "SubstoryCumulativeSummaryPrompt",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "ChapterSummaryContext": (".context", "ChapterSummaryContext"),
    "ChapterSummaryPrompt": (".prompt", "ChapterSummaryPrompt"),
    "PostWritingEngine": (".engine", "PostWritingEngine"),
    "SubstoryCumulativeSummaryContext": (".context", "SubstoryCumulativeSummaryContext"),
    "SubstoryCumulativeSummaryPrompt": (".prompt", "SubstoryCumulativeSummaryPrompt"),
}

if TYPE_CHECKING:
    from .context import ChapterSummaryContext, SubstoryCumulativeSummaryContext
    from .engine import PostWritingEngine
    from .prompt import ChapterSummaryPrompt, SubstoryCumulativeSummaryPrompt


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
