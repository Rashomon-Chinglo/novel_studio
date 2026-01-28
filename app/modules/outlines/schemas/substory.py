from pydantic import BaseModel, ConfigDict, Field


class SubstoryActionNode(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cause: str = Field(alias="起因")
    process: str = Field(alias="经过")
    effect: str = Field(alias="结果")
    exchange: str = Field(alias="变化")
    context: str | None = Field(alias="背景与可能的变化")

    def prompt(self, index: int | None = None):
        action_node = self.model_dump(exclude_none=True, by_alias=True)
        content = "\n\n".join([f"- **{k}**: {v}" for k, v in action_node.items()])
        _index = f"{index}" if index else ""
        return f"<卷钢逻辑节点{_index}>\n{content}\n</卷钢逻辑节点{_index}>"


class Substory(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    substory_title: str = Field(alias="篇章标题")
    logic_nodes: list[SubstoryActionNode] = Field(alias="逻辑节点列表", min_length=1)
    core_conflict: str = Field(alias="核心冲突")
    status_change: str = Field(alias="状态变化")

    def prompt(
        self,
        exclude: list[str] | None = None,
    ) -> str:
        if exclude is None:
            exclude = []
        substory = self.model_dump(
            exclude=set(["logic_nodes", *exclude]),
            exclude_none=True,
            by_alias=True,
        )
        logic_nodes_prompt = "\n".join(
            [node.prompt(index + 1) for index, node in enumerate(self.logic_nodes)]
        )
        content = "\n\n".join([f"## {k}\n{v}" for k, v in substory.items()])
        return f"<篇章逻辑>\n{content}\n<逻辑节点列表>\n{logic_nodes_prompt}\n</逻辑节点列表>\n</篇章逻辑>"
