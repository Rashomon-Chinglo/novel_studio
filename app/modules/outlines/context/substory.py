from app.modules.base.context import BaseContext
from ..schemas.bible import Bible


def _format_bible(bible: Bible) -> str:
    return bible.model_dump_json(
        include=[
            "worldview_tone",
            "main_conflict",
            "ending_vision",
            "key_roles_summary",
        ]
    )


class BrainstormContext(BaseContext):
    history: list[str] = []
    user_input: str = ""
    bible: Bible

    def format_bible(self) -> str:
        return _format_bible(self.bible)


class SubstoryContext(BaseContext):
    history: list[str] = []
    bible: Bible

    def format_bible(self) -> str:
        return _format_bible(self.bible)
