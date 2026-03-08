import pytest
from inline_snapshot import snapshot

from app.modules.outlines.prompts.substory import SubstoryBrainstormPrompt
from app.modules.outlines.prompts.substory import SubstoryGeneratePrompt
from app.modules.outlines.context.substory import SubstoryBrainstormContext
from app.modules.outlines.context.substory import SubstoryGenerateContext
from langchain_core.prompts import ChatPromptTemplate


@pytest.fixture()
def substory_brainstorm_prompt() -> SubstoryBrainstormPrompt:
    return SubstoryBrainstormPrompt()


@pytest.fixture()
def substory_generate_prompt() -> SubstoryGeneratePrompt:
    return SubstoryGeneratePrompt()


@pytest.mark.unit()
def test_substory_brainstorm_prompt_template(
    substory_brainstorm_prompt: SubstoryBrainstormPrompt,
) -> None:
    assert len(substory_brainstorm_prompt.template) == snapshot(699)


@pytest.mark.unit()
def test_substory_brainstorm_prompt_build_variables(
    substory_brainstorm_prompt: SubstoryBrainstormPrompt,
    substory_brainstorm_context: SubstoryBrainstormContext,
) -> None:
    assert substory_brainstorm_prompt.build_variables(substory_brainstorm_context) == snapshot(
        {
            "history": """\
test
history\
""",
            "user_input": "test",
            "overview_outline": """\
<小说总纲>
## 书名
测试小说名

## 梗概
这是一个测试用的核心梗概，描述了主角的冒险故事。

## 核心卖点，爽点
无敌流，快节奏，系统文

## 世界观基调
赛博朋克风格废土世界，基调灰暗但充满希望

## 主线冲突
底层平民与财阀高层的生存资源争夺战

## 结局愿景
主角推翻财阀，建立新的秩序

## 主角们的简要概述
主角李四是孤儿，配角王五是他的黑客导师
</小说总纲>\
""",
        }
    )


@pytest.mark.unit()
def test_substory_brainstorm_prompt_prompt(
    substory_brainstorm_prompt: SubstoryBrainstormPrompt,
) -> None:
    assert isinstance(substory_brainstorm_prompt.prompt, ChatPromptTemplate)
    assert substory_brainstorm_prompt.prompt.input_variables == snapshot(
        ["history", "overview_outline", "user_input"]
    )


@pytest.mark.unit()
def test_substory_brainstorm_prompt_version(
    substory_brainstorm_prompt: SubstoryBrainstormPrompt,
) -> None:
    assert substory_brainstorm_prompt.version() == snapshot("1.0.0")


@pytest.mark.unit()
def test_substory_generate_prompt_template(
    substory_generate_prompt: SubstoryGeneratePrompt,
) -> None:
    assert len(substory_generate_prompt.template) == snapshot(965)


@pytest.mark.unit()
def test_substory_generate_prompt_build_variables(
    substory_generate_prompt: SubstoryGeneratePrompt,
    substory_generate_context: SubstoryGenerateContext,
) -> None:
    assert substory_generate_prompt.build_variables(substory_generate_context) == snapshot(
        {
            "overview_outline": """\
<小说总纲>
## 书名
测试小说名

## 梗概
这是一个测试用的核心梗概，描述了主角的冒险故事。

## 核心卖点，爽点
无敌流，快节奏，系统文

## 世界观基调
赛博朋克风格废土世界，基调灰暗但充满希望

## 主线冲突
底层平民与财阀高层的生存资源争夺战

## 结局愿景
主角推翻财阀，建立新的秩序

## 主角们的简要概述
主角李四是孤儿，配角王五是他的黑客导师
</小说总纲>\
""",
            "conversation_text": """\
test
history\
""",
        }
    )


@pytest.mark.unit()
def test_substory_generate_prompt_prompt(substory_generate_prompt: SubstoryGeneratePrompt) -> None:
    assert isinstance(substory_generate_prompt.prompt, ChatPromptTemplate)
    assert substory_generate_prompt.prompt.input_variables == snapshot(
        ["conversation_text", "overview_outline"]
    )


@pytest.mark.unit()
def test_substory_generate_prompt_version(substory_generate_prompt: SubstoryGeneratePrompt) -> None:
    assert substory_generate_prompt.version() == snapshot("1.0.0")
