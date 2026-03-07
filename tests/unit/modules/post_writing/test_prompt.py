import pytest
from inline_snapshot import snapshot
from langchain_core.prompts import ChatPromptTemplate

from app.modules.post_writing.context import ChapterSummaryContext, SubstoryCumulativeSummaryContext
from app.modules.post_writing.prompt import ChapterSummaryPrompt, SubstoryCumulativeSummaryPrompt


@pytest.fixture()
def chapter_summary_prompt() -> ChapterSummaryPrompt:
    return ChapterSummaryPrompt()


@pytest.fixture()
def substory_cumulative_summary_prompt() -> SubstoryCumulativeSummaryPrompt:
    return SubstoryCumulativeSummaryPrompt()


@pytest.mark.unit()
def test_chapter_summary_prompt_template(chapter_summary_prompt: ChapterSummaryPrompt) -> None:
    assert len(chapter_summary_prompt.template) == snapshot(763)


@pytest.mark.unit()
def test_chapter_summary_prompt_build_variables(
    chapter_summary_prompt: ChapterSummaryPrompt,
    chapter_summary_context: ChapterSummaryContext,
) -> None:
    assert chapter_summary_prompt.build_variables(chapter_summary_context) == snapshot(
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
            "substory_outline": """\
<篇章逻辑>
## 篇章标题
第一卷：初入废土

## 核心冲突
主角能否在贫民窟的黑帮火拼中活下来

## 状态变化
从手无寸铁的平民变为觉醒异能的战士
<逻辑节点列表>
<卷钢逻辑节点1>
- **起因**: 黑帮抢夺贫民窟的净水装置

- **经过**: 主角为了保护妹妹被卷入冲突，意外接触到神秘源石

- **结果**: 主角觉醒了雷电异能

- **变化**: 平静的生活被打破，被黑帮追杀

- **背景与可能的变化**: 此时全城的警方力量已被财阀抽走
</卷钢逻辑节点1>
</逻辑节点列表>
</篇章逻辑>\
""",
            "original_logic_nodes": """\
<章节逻辑节点>
<卷钢逻辑节点>
- **起因**: 黑帮抢夺贫民窟的净水装置

- **经过**: 主角为了保护妹妹被卷入冲突，意外接触到神秘源石

- **结果**: 主角觉醒了雷电异能

- **变化**: 平静的生活被打破，被黑帮追杀

- **背景与可能的变化**: 此时全城的警方力量已被财阀抽走
</卷钢逻辑节点>
</章节逻辑节点>\
""",
            "chapter_outline": """\
<章节>
## 章节序号
1

## 章节标题
雨夜的枪声

## 章节主题色调
紧张、压抑

## 章节开头的悬念
一颗子弹擦过李四的耳边，打碎了身后的净水器

## 章节结尾的悬念
李四倒在血泊中，眼看黑帮老大举起了枪，突然他的手心闪烁起蓝色的电光……
<场景列表>
<场景1>
- **场景地点**: 贫民窟的废弃工厂巷道

- **场景时间及环境**: 深夜，暴雨倾盆

- **场景中的人物**: 李四,黑帮小喽啰,妹妹小红

- **本场细的目标**: 李四试图带着妹妹逃离黑帮的包围圈

- **本场戏承接substory的哪一条**: 承接卷一节点1：黑帮火拼爆发
<场景节拍列表>
<场景节拍1>
- **描写技法**: 动作

- **情绪**: 激昂

- **具体的剧情动作点**: 李四翻滚躲开射击，同时抛出一枚自制电磁脉冲手雷
</场景节拍1>
</场景节拍列表>
</场景1>
</场景列表>
</章节>\
""",
            "cumulative_substory_summary": """\
<卷内进度总结>
黑帮大举搜索贫民窟，李四处于极度恐惧中。
</卷内进度总结>\
""",
            "pre_chapter_summary": """\
<章节总结>
上一章讲了李四逃入废弃工厂，暂时躲过了追捕。
</章节总结>\
""",
            "chapter_content": """\
<章节正文>
李四喘着粗气，靠在冰冷的墙上。
外面传来了杂乱的脚步声。
</章节正文>\
""",
        }
    )


@pytest.mark.unit()
def test_chapter_summary_prompt_prompt(chapter_summary_prompt: ChapterSummaryPrompt) -> None:
    assert isinstance(chapter_summary_prompt.prompt, ChatPromptTemplate)


@pytest.mark.unit()
def test_chapter_summary_prompt_version(chapter_summary_prompt: ChapterSummaryPrompt) -> None:
    assert chapter_summary_prompt.version() == snapshot("1.0.0")


@pytest.mark.unit()
def test_substory_cumulative_summary_prompt_template(
    substory_cumulative_summary_prompt: SubstoryCumulativeSummaryPrompt,
) -> None:
    assert len(substory_cumulative_summary_prompt.template) == snapshot(659)


@pytest.mark.unit()
def test_substory_cumulative_summary_prompt_build_variables(
    substory_cumulative_summary_prompt: SubstoryCumulativeSummaryPrompt,
    substory_cumulative_summary_context: SubstoryCumulativeSummaryContext,
) -> None:
    assert substory_cumulative_summary_prompt.build_variables(
        substory_cumulative_summary_context
    ) == snapshot(
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
            "substory_outline": """\
<篇章逻辑>
## 篇章标题
第一卷：初入废土

## 核心冲突
主角能否在贫民窟的黑帮火拼中活下来

## 状态变化
从手无寸铁的平民变为觉醒异能的战士
<逻辑节点列表>
<卷钢逻辑节点1>
- **起因**: 黑帮抢夺贫民窟的净水装置

- **经过**: 主角为了保护妹妹被卷入冲突，意外接触到神秘源石

- **结果**: 主角觉醒了雷电异能

- **变化**: 平静的生活被打破，被黑帮追杀

- **背景与可能的变化**: 此时全城的警方力量已被财阀抽走
</卷钢逻辑节点1>
</逻辑节点列表>
</篇章逻辑>\
""",
            "cumulative_substory_summary": """\
<卷内进度总结>
黑帮大举搜索贫民窟，李四处于极度恐惧中。
</卷内进度总结>\
""",
            "current_chapter_summary": """\
<章节总结>
上一章讲了李四逃入废弃工厂，暂时躲过了追捕。
</章节总结>\
""",
        }
    )


@pytest.mark.unit()
def test_substory_cumulative_summary_prompt_prompt(
    substory_cumulative_summary_prompt: SubstoryCumulativeSummaryPrompt,
) -> None:
    assert isinstance(substory_cumulative_summary_prompt.prompt, ChatPromptTemplate)


@pytest.mark.unit()
def test_substory_cumulative_summary_prompt_version(
    substory_cumulative_summary_prompt: SubstoryCumulativeSummaryPrompt,
) -> None:
    assert substory_cumulative_summary_prompt.version() == snapshot("1.0.0")
