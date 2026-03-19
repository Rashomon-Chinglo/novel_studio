from pydantic import BaseModel

from ..schemas.bible import Bible


class SubstoryBrainstormContext(BaseModel):
    history: list[str]
    user_input: str
    bible: Bible


class SubstoryGenerateContext(BaseModel):
    messages: list[str]
    bible: Bible
