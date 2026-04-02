from importlib import import_module
from types import ModuleType
from typing import TYPE_CHECKING, Any

__all__ = [
    "SqlAlchemyUnitOfWork",
    "get_vector_store",
    "init_db_schema",
    "initialize_persistence",
]

_EXPORTS: dict[str, tuple[str, str] | ModuleType] = {
    "SqlAlchemyUnitOfWork": (".db.unit_of_work", "SqlAlchemyUnitOfWork"),
    "get_vector_store": (".db", "get_vector_store"),
    "init_db_schema": (".db", "init_db_schema"),
    "initialize_persistence": (".db", "initialize_persistence"),
}

if TYPE_CHECKING:
    from .db import get_vector_store, init_db_schema, initialize_persistence
    from .db.unit_of_work import SqlAlchemyUnitOfWork


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]  # type: ignore[misc]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
