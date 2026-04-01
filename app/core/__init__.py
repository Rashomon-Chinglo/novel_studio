from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "BASE_DIR",
    "DATA_DIR",
    "Settings",
    "get_llm",
    "settings",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "BASE_DIR": (".config", "BASE_DIR"),
    "DATA_DIR": (".config", "DATA_DIR"),
    "Settings": (".config", "Settings"),
    "get_llm": (".llm", "get_llm"),
    "settings": (".config", "settings"),
}

if TYPE_CHECKING:
    from .config import BASE_DIR, DATA_DIR, Settings, settings
    from .llm import get_llm


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
