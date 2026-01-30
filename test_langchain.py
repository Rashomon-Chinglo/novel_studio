from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from app.core.llm import get_llm


class Bible(BaseModel):
    title: str = Field(description="书名")
    logline: str = Field(description="梗概，一句话梗概（尽量做到引人眼球，30-50字，必须包含钩子）")

    marketing_hook: str = Field(description="核心卖点，爽点")
    worldview_tone: str = Field(description="世界观基调，例如[赛博休闲]，[女尊恋爱]，[无限流]等")
    main_conflict: str = Field(description="主线冲突")
    ending_vision: str = Field(description="结局愿景")

    key_roles_summary: str = Field(description="主角们的简要概述")


def get_brainstorm_chain(prompt: ChatPromptTemplate):
    llm = get_llm()
    structured_llm = prompt | llm | StrOutputParser()
    return structured_llm


def get_bible_chain(prompt: ChatPromptTemplate):
    llm = get_llm()

    # Note: method="json_mode" is used, which typically requires the model to be explicitly
    # instructed to output JSON in the prompt, though libraries may handle some of this.
    structured_llm = prompt | llm.with_structured_output(
        Bible, method="function_calling", include_raw=True
    )

    return structured_llm


def test_structured_output():
    # 'json_mode' often requires the word "JSON" in the prompt to work reliably with OpenAI
    prompt = ChatPromptTemplate.from_template("Generate a creative novel outline about {topic}.")
    chain = get_bible_chain(prompt)

    print("Invoking chain...")
    result = chain.invoke({"topic": "a detective who can talk to ghosts"})

    print("Raw Result:", result)

    # When include_raw=True, the output is typically a dictionary containing 'parsed', 'raw', etc.
    parsed_output = None
    if isinstance(result, dict) and "parsed" in result:
        parsed_output = result["parsed"]
    elif hasattr(result, "parsed"):
        parsed_output = result.parsed
    else:
        # Fallback if the structure is different (e.g. just the object)
        parsed_output = result

    if parsed_output is None:
        print("Error: Could not find parsed output in result.")
        return

    print(f"\nSuccessfully parsed output into type: {type(parsed_output)}")

    assert isinstance(parsed_output, Bible), f"Expected Bible instance, got {type(parsed_output)}"
    print(f"Title: {parsed_output.title}")
    print(f"Logline: {parsed_output.logline}")
    print("\nTest passed successfully!")


if __name__ == "__main__":
    test_structured_output()
