from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "ChapterSceneWritingContext",
    "ChapterWritingContext",
    "MaterialProvider",
    "SceneChunk",
    "WritingEngine",
    "WrittenChapter",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "ChapterSceneWritingContext": (".context", "ChapterSceneWritingContext"),
    "ChapterWritingContext": (".context", "ChapterWritingContext"),
    "MaterialProvider": (".providers", "MaterialProvider"),
    "SceneChunk": (".schemas", "SceneChunk"),
    "WritingEngine": (".engine", "WritingEngine"),
    "WrittenChapter": (".schemas", "WrittenChapter"),
}

if TYPE_CHECKING:
    from .context import ChapterSceneWritingContext, ChapterWritingContext
    from .engine import WritingEngine
    from .providers import MaterialProvider
    from .schemas import SceneChunk, WrittenChapter


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
