from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "MaterialService",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "MaterialService": (".materials", "MaterialService"),
}

if TYPE_CHECKING:
    from .materials import MaterialService


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
