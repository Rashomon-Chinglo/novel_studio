from abc import ABC, abstractmethod

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel


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
