from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "BibleRepository",
    "ChapterOutlineRepository",
    "SubstoryRepository",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "BibleRepository": (".bible", "BibleRepository"),
    "ChapterOutlineRepository": (".chapter", "ChapterOutlineRepository"),
    "SubstoryRepository": (".substory", "SubstoryRepository"),
}

if TYPE_CHECKING:
    from .bible import BibleRepository
    from .chapter import ChapterOutlineRepository
    from .substory import SubstoryRepository


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
