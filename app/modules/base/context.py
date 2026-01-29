from pydantic import BaseModel


class BaseContext(BaseModel):
    def to_prompt_variables(self) -> dict[str, str]:
        raise NotImplementedError
