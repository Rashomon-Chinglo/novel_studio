from app.modules.base.context import BaseContext


class BibleBrainstormContext(BaseContext):
    history: list[str]
    user_input: str


class BibleGenerateContext(BaseContext):
    messages: list[str]
