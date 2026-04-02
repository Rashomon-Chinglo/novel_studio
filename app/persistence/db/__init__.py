from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "Base",
    "SessionFactory",
    "engine",
    "get_vector_store",
    "init_db_schema",
    "initialize_persistence",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "Base": (".base", "Base"),
    "SessionFactory": (".engine", "SessionFactory"),
    "engine": (".engine", "engine"),
    "get_vector_store": (".vector", "get_vector_store"),
    "initialize_persistence": (".init", "initialize_persistence"),
    "init_db_schema": (".schema", "init_db_schema"),
}

if TYPE_CHECKING:
    from .base import Base
    from .engine import SessionFactory, engine
    from .init import initialize_persistence
    from .schema import init_db_schema
    from .vector import get_vector_store


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
