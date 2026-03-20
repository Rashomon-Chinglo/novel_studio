from typing import Any, override

from langchain_core.callbacks import (
    CallbackManagerForLLMRun,
)
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import RunnableSerializable
from pydantic import Field


def extract_texts(messages: list[BaseMessage]) -> list[str]:
    return [message.content for message in messages if isinstance(message.content, str)]


class StructuredOutputRunnable[T](RunnableSerializable[PromptValue, T]):
    owner: "FakeLLM"

    def invoke(self, input: PromptValue, config: object = None, **kwargs: Any) -> T:
        self.owner.structured_prompts.append(extract_texts(input.to_messages()))
        return self.owner.next_structured_response()

    async def ainvoke(self, input: PromptValue, config: object = None, **kwargs: Any) -> T:
        self.owner.structured_prompts.append(extract_texts(input.to_messages()))
        return self.owner.next_structured_response()


class FakeLLM[R](FakeMessagesListChatModel):
    plain_prompts: list[list[str]] = Field(default_factory=list)
    structured_prompts: list[list[str]] = Field(default_factory=list)
    structured_responses: list[R] = Field(default_factory=list)
    structured_output_requests: list[dict[str, Any]] = Field(default_factory=list)
    structured_index: int = 0

    def next_structured_response(self) -> R:
        if not self.structured_responses:
            raise AssertionError("No structured responses configured for fake LLM.")
        response = self.structured_responses[self.structured_index]
        self.structured_index = (self.structured_index + 1) % len(self.structured_responses)
        return response

    @override
    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        self.plain_prompts.append(extract_texts(messages))
        return super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)

    def with_structured_output(  # type: ignore[override]
        self,
        schema: type[R],
        *,
        include_raw: bool = False,
        **kwargs: Any,
    ) -> StructuredOutputRunnable[R]:
        self.structured_output_requests.append(
            {
                "schema": schema,
                "include_raw": include_raw,
                **kwargs,
            }
        )
        return StructuredOutputRunnable(owner=self)
