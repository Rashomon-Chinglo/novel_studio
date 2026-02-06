from pydantic import BaseModel


class BibleBrainstormContext(BaseModel):
    history: list[str]
    user_input: str


class BibleGenerateContext(BaseModel):
    messages: list[str]
