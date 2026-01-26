from pydantic import BaseModel, Field


class SubstoryActionNode(BaseModel):
    cause: str = Field(alias="起因")
    process: str = Field(alias="经过")
    effect: str = Field(alias="结果")
    exchange: str = Field(alias="变化")
    context: str | None = Field(alias="背景与可能的变化")

    def prompt(self, index: int | None = None):
        action_node = self.model_dump(exclude_none=True, by_alias=True)
        content = "\n\n".join([f"- **{k}**: {v}" for k, v in action_node.items()])
        index = f"{index}" if index else ""
        return f"<卷钢逻辑节点{index}>\n{content}\n</卷钢逻辑节点{index}>"


class Substory(BaseModel):
    substory_title: str = Field(alias="篇章标题")
    logic_nodes: list[SubstoryActionNode] = Field(alias="逻辑节点列表", min_length=1)
    core_conflict: str = Field(alias="核心冲突")
    status_change: str = Field(alias="状态变化")

    def prompt(
        self, exclude: list[str] = [], node_range: tuple[int, int] | None = None
    ):
        substory = self.model_dump(
            exclude=["logic_nodes", *exclude],
            exclude_none=True,
            by_alias=True,
        )
        if node_range:
            logic_nodes = self.logic_nodes[node_range[0] : node_range[1]]
        else:
            logic_nodes = self.logic_nodes
        logic_nodes_prompt = "\n".join(
            [node.prompt(index + 1) for index, node in enumerate(logic_nodes)]
        )
        content = "\n\n".join([f"## {k}\n{v}" for k, v in substory.items()])
        return f"<篇章逻辑>\n{content}\n<逻辑节点列表>\n{logic_nodes_prompt}\n</逻辑节点列表>\n</篇章逻辑>"
