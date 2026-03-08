import pytest
from inline_snapshot import snapshot
from app.modules.outlines.schemas.substory import (
    SubstoryActionNode,
    Substory,
    ChapterOriginalSubstoryNodes,
)

@pytest.fixture
def action_node():
    return SubstoryActionNode(
        cause="黑帮抢夺贫民窟的净水装置",
        process="主角为了保护妹妹被卷入冲突，意外接触到神秘源石",
        effect="主角觉醒了雷电异能",
        exchange="平静的生活被打破，被黑帮追杀",
        context="此时全城的警方力量已被财阀抽走",
    )

@pytest.fixture
def substory(action_node):
    return Substory(
        substory_title="第一卷：初入废土",
        core_conflict="主角能否在贫民窟的黑帮火拼中活下来",
        status_change="从手无寸铁的平民变为觉醒异能的战士",
        logic_nodes=[action_node],
    )

@pytest.fixture
def chapter_nodes(action_node):
    return ChapterOriginalSubstoryNodes(nodes=[action_node])

@pytest.mark.unit
def test_substory_action_node_prompt(action_node) -> None:
    assert action_node.prompt(index=1) == snapshot("""\
<卷钢逻辑节点1>
- **起因**: 黑帮抢夺贫民窟的净水装置

- **经过**: 主角为了保护妹妹被卷入冲突，意外接触到神秘源石

- **结果**: 主角觉醒了雷电异能

- **变化**: 平静的生活被打破，被黑帮追杀

- **背景与可能的变化**: 此时全城的警方力量已被财阀抽走
</卷钢逻辑节点1>\
""")

@pytest.mark.unit
def test_substory_prompt(substory) -> None:
    assert substory.prompt() == snapshot("""\
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
""")

@pytest.mark.unit
def test_chapter_original_substory_nodes_prompt(chapter_nodes):
    assert chapter_nodes.prompt() == snapshot("""\
<章节逻辑节点>
<卷钢逻辑节点>
- **起因**: 黑帮抢夺贫民窟的净水装置

- **经过**: 主角为了保护妹妹被卷入冲突，意外接触到神秘源石

- **结果**: 主角觉醒了雷电异能

- **变化**: 平静的生活被打破，被黑帮追杀

- **背景与可能的变化**: 此时全城的警方力量已被财阀抽走
</卷钢逻辑节点>
</章节逻辑节点>\
""")
