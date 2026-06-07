"""Outline API schemas."""

from pydantic import BaseModel, Field

from app.modules.outlines.schemas import Bible, Substory


class BrainstormBibleRequest(BaseModel):
    history: list[str] = Field(default_factory=list)
    user_input: str


class BrainstormSubstoryRequest(BaseModel):
    history: list[str] = Field(default_factory=list)
    user_input: str
    bible_id: str


class BrainstormResponse(BaseModel):
    content: str


class CreateBibleRequest(BaseModel):
    messages: list[str]


class CreateBibleResponse(BaseModel):
    bible_id: str


class BibleResponse(BaseModel):
    bible: Bible


class CreateSubstoryRequest(BaseModel):
    bible_id: str
    substory_order_index: int
    messages: list[str]


class CreateSubstoryResponse(BaseModel):
    substory_id: str


class SubstoryResponse(BaseModel):
    substory: Substory
