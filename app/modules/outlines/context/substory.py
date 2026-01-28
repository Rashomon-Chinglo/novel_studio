from app.modules.base.context import BaseContext

from ..schemas.bible import Bible


class SubstoryBrainstormContext(BaseContext):
    history: list[str]
    user_input: str
    bible: Bible


class SubstoryGenerateContext(BaseContext):
    history: list[str]
    bible: Bible
