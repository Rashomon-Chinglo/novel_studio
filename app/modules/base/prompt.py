from abc import ABC, abstractmethod
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate


class PromptTemplate[T: BaseModel](ABC):
    @property
    @abstractmethod
    def template(self) -> str:
        pass

    @property
    @abstractmethod
    def prompt(self) -> ChatPromptTemplate:
        pass

    @abstractmethod
    def build_variables(self, context: T) -> dict[str, str]:
        pass

    @abstractmethod
    def version(self) -> str:
        pass
