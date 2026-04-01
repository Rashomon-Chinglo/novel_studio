from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "ExtractedResult",
    "MaterialEngine",
    "MaterialSnippet",
    "MaterialsMiningContext",
    "MaterialsMiningPrompt",
    "get_mining_chain",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "ExtractedResult": (".schemas", "ExtractedResult"),
    "MaterialEngine": (".engine", "MaterialEngine"),
    "MaterialSnippet": (".schemas", "MaterialSnippet"),
    "MaterialsMiningContext": (".context", "MaterialsMiningContext"),
    "MaterialsMiningPrompt": (".prompt", "MaterialsMiningPrompt"),
    "get_mining_chain": (".chain", "get_mining_chain"),
}

if TYPE_CHECKING:
    from .chain import get_mining_chain
    from .context import MaterialsMiningContext
    from .engine import MaterialEngine
    from .prompt import MaterialsMiningPrompt
    from .schemas import ExtractedResult, MaterialSnippet


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
