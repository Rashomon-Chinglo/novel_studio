from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "get_bible_brainstorm_chain",
    "get_bible_chain",
    "get_chapter_blueprint_chain",
    "get_chapter_brainstorm_chain",
    "get_chapter_scene_chain",
    "get_substory_brainstorm_chain",
    "get_substory_chain",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "get_bible_brainstorm_chain": (".bible", "get_brainstorm_chain"),
    "get_bible_chain": (".bible", "get_bible_chain"),
    "get_chapter_blueprint_chain": (".chapter", "get_chapter_blueprint_chain"),
    "get_chapter_brainstorm_chain": (".chapter", "get_chapter_brainstorm_chain"),
    "get_chapter_scene_chain": (".chapter", "get_chapter_scene_chain"),
    "get_substory_brainstorm_chain": (".substory", "get_brainstorm_chain"),
    "get_substory_chain": (".substory", "get_substory_chain"),
}

if TYPE_CHECKING:
    from .bible import get_bible_chain
    from .bible import get_brainstorm_chain as get_bible_brainstorm_chain
    from .chapter import (
        get_chapter_blueprint_chain,
        get_chapter_brainstorm_chain,
        get_chapter_scene_chain,
    )
    from .substory import get_brainstorm_chain as get_substory_brainstorm_chain
    from .substory import get_substory_chain


def __getattr__(name: str) -> Any:
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
