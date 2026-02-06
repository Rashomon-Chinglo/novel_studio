from typing import ClassVar

from pydantic import BaseModel, Field


class SubstoryActionNode(BaseModel):
    _prompt_labels: ClassVar[dict[str, str]] = {
        "cause": "起因",
        "process": "经过",
        "effect": "结果",
        "exchange": "变化",
        "context": "背景与可能的变化",
    }

    cause: str
    process: str
    effect: str
    exchange: str
    context: str | None = None

    def prompt(self, index: int | None = None):
        data = self.model_dump(exclude_none=True)
        action_node = {self._prompt_labels.get(k, k): v for k, v in data.items()}
        content = "\n\n".join([f"- **{k}**: {v}" for k, v in action_node.items()])
        _index = f"{index}" if index else ""
        return f"<卷钢逻辑节点{_index}>\n{content}\n</卷钢逻辑节点{_index}>"


class Substory(BaseModel):
    _prompt_labels: ClassVar[dict[str, str]] = {
        "substory_title": "篇章标题",
        "logic_nodes": "逻辑节点列表",
        "core_conflict": "核心冲突",
        "status_change": "状态变化",
    }

    substory_title: str
    logic_nodes: list[SubstoryActionNode] = Field(min_length=1)
    core_conflict: str
    status_change: str

    def prompt(
        self,
        exclude: list[str] | None = None,
    ) -> str:
        if exclude is None:
            exclude = []
        data = self.model_dump(
            exclude=set(["logic_nodes", *exclude]),
            exclude_none=True,
        )
        substory = {self._prompt_labels.get(k, k): v for k, v in data.items()}
        logic_nodes_prompt = "\n".join(
            [node.prompt(index + 1) for index, node in enumerate(self.logic_nodes)]
        )
        content = "\n\n".join([f"## {k}\n{v}" for k, v in substory.items()])
        return f"<篇章逻辑>\n{content}\n<逻辑节点列表>\n{logic_nodes_prompt}\n</逻辑节点列表>\n</篇章逻辑>"


class ChapterOriginalSubstoryNodes(BaseModel):
    """章节对应的原始卷钢逻辑节点列表"""

    nodes: list[SubstoryActionNode] = Field(min_length=1)

    def prompt(self) -> str:
        nodes_prompt = "\n".join([node.prompt() for node in self.nodes])
        return f"<章节逻辑节点>\n{nodes_prompt}\n</章节逻辑节点>"
