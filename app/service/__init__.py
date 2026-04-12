from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "MaterialService",
    "PostWritingService",
    "WorkflowRunService",
    "WritingService",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "MaterialService": (".materials", "MaterialService"),
    "PostWritingService": (".post_writing", "PostWritingService"),
    "WorkflowRunService": (".workflow", "WorkflowRunService"),
    "WritingService": (".writing", "WritingService"),
}

if TYPE_CHECKING:
    from .materials import MaterialService
    from .post_writing import PostWritingService
    from .workflow import WorkflowRunService
    from .writing import WritingService


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
