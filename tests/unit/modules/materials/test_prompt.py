import pytest
from inline_snapshot import snapshot
from langchain_core.prompts import ChatPromptTemplate

from app.modules.materials.context import MaterialsMiningContext
from app.modules.materials.prompt import MaterialsMiningPrompt


@pytest.fixture()
def materials_prompt() -> MaterialsMiningPrompt:
    return MaterialsMiningPrompt()


@pytest.mark.unit()
def test_materials_prompt_template(materials_prompt: MaterialsMiningPrompt) -> None:
    assert len(materials_prompt.template) == snapshot(688)


@pytest.mark.unit()
def test_materials_prompt_build_variables(materials_prompt: MaterialsMiningPrompt) -> None:
    context = MaterialsMiningContext(
        text="这是一个测试文本。",
    )
    assert materials_prompt.build_variables(context) == snapshot({"text": "这是一个测试文本。"})


@pytest.mark.unit()
def test_materials_prompt_prompt(materials_prompt: MaterialsMiningPrompt) -> None:
    assert isinstance(materials_prompt.prompt, ChatPromptTemplate)
    assert materials_prompt.prompt.input_variables == snapshot(["text"])


@pytest.mark.unit()
def test_materials_prompt_version(materials_prompt: MaterialsMiningPrompt) -> None:
    assert materials_prompt.version() == snapshot("1.0.0")
