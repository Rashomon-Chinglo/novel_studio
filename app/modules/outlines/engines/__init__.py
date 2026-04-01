from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "BibleEngine",
    "ChapterEngine",
    "SubstoryEngine",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "BibleEngine": (".bible", "BibleEngine"),
    "ChapterEngine": (".chapter", "ChapterEngine"),
    "SubstoryEngine": (".substory", "SubstoryEngine"),
}

if TYPE_CHECKING:
    from .bible import BibleEngine
    from .chapter import ChapterEngine
    from .substory import SubstoryEngine


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
