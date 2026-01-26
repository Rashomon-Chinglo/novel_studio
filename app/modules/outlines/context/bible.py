from app.modules.base.context import BaseContext


class BrainstormContext(BaseContext):
    history: list[str] = []
    user_input: str


class BibleContext(BaseContext):
    messages: list[str]
