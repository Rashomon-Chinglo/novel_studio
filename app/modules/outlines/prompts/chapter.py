from langchain_core.prompts import ChatPromptTemplate

from app.modules.base.prompt import PromptTemplate

from ..context.chapter import (
    ChapterBlueprintBrainstormContext,
    ChapterBlueprintContext,
    ChapterSceneContext,
)


class ChapterBlueprintPrompt(PromptTemplate[ChapterBlueprintContext]):
    @property
    def template(self) -> str:
        return """
        # 角色
        你是一位拥有深厚编剧功底的网文大纲架构师。你能够将抽象的因果逻辑转化为具备画面感和节奏感的场景序列。

        # 背景
        {overview_outline}

        {substory_outline}

        {cumulative_substory_summary}

        {pre_chapter_summary}

        # 任务
        请**根据以下逻辑节点**，结合上述背景，规划本章节（Chapter）的场景骨架。
        {logic_nodes_to_process}
        """

    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
            ]
        )

    def build_variables(self, context: ChapterBlueprintContext) -> dict[str, str]:
        logic_nodes_to_process = "\n".join(
            [node.prompt() for node in context.logic_nodes_to_process]
        )
        return {
            "overview_outline": context.bible.prompt(),
            "substory_outline": context.substory.prompt(),
            "cumulative_substory_summary": f"<卷内进度>\n{context.cumulative_substory_summary}\n</卷内进度>",
            "pre_chapter_summary": f"<上章总结>\n{context.pre_chapter_summary}\n</上章总结>",
            "logic_nodes_to_process": f"<本章逻辑节点>\n{logic_nodes_to_process}\n</本章逻辑节点>",
        }


class ChapterBlueprintBrainstormPrompt(PromptTemplate[ChapterBlueprintBrainstormContext]):
    @property
    def template(self) -> str:
        return """
        # 角色
        你是一位拥有深厚编剧功底的网文大纲架构师。你能够将抽象的因果逻辑转化为具备画面感和节奏感的场景序列。

        # 背景
        {overview_outline}

        {substory_outline}

        {cumulative_substory_summary}

        {pre_chapter_summary}

        # 任务
        请**根据以下逻辑节点**与**用户头脑风暴记录**，结合上述背景，规划本章节（Chapter）的场景骨架。
        {chapter_blueprint}

        {logic_nodes_to_process}
        """

    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
                ("placeholder", "{conversation_history}"),
                ("human", "{user_input}"),
            ]
        )

    def build_variables(self, context: ChapterBlueprintBrainstormContext) -> dict[str, str]:
        logic_nodes_to_process = "\n".join(
            [node.prompt() for node in context.logic_nodes_to_process]
        )
        conversation_history = "\n".join(context.history) if context.history else "(无历史记录)"

        return {
            "overview_outline": context.bible.prompt(),
            "substory_outline": context.substory.prompt(),
            "chapter_blueprint": context.chapter_blueprint.prompt(),
            "cumulative_substory_summary": f"<卷内进度>\n{context.cumulative_substory_summary}\n</卷内进度>",
            "pre_chapter_summary": f"<上章总结>\n{context.pre_chapter_summary}\n</上章总结>",
            "logic_nodes_to_process": f"<本章逻辑节点>\n{logic_nodes_to_process}\n</本章逻辑节点>",
            "conversation_history": f"<头脑风暴记录>\n{conversation_history}\n</头脑风暴记录>",
            "user_input": context.user_input,
        }


class ChapterScenePrompt(PromptTemplate[ChapterSceneContext]):
    @property
    def template(self) -> str:
        return """
        # 角色
        你是一位拥有深厚编剧功底的网文大纲架构师。你能够将抽象的因果逻辑转化为具备画面感和节奏感的场景序列。

        # 背景
        {overview_outline}

        {substory_outline}

        {cumulative_substory_summary}

        {pre_chapter_summary}

        {last_scene_beat}
        # 任务
        请**根据以下逻辑节点**，**章节蓝图**，**场景骨架**，结合上述背景，规划出场景骨架的详细内容。
        {chapter_blueprint}

        {logic_nodes_to_process}

        {scene_blueprint}
        """

    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
            ]
        )

    def build_variables(self, context: ChapterSceneContext) -> dict[str, str]:
        logic_nodes_to_process = "\n".join(
            [node.prompt() for node in context.logic_nodes_to_process]
        )
        return {
            "overview_outline": context.bible.prompt(),
            "substory_outline": context.substory.prompt(),
            "chapter_blueprint": context.chapter_blueprint.prompt(),
            "cumulative_substory_summary": f"<卷内进度>\n{context.cumulative_substory_summary}\n</卷内进度>",
            "pre_chapter_summary": f"<上章总结>\n{context.pre_chapter_summary}\n</上章总结>",
            "logic_nodes_to_process": f"<本章逻辑节点>\n{logic_nodes_to_process}\n</本章逻辑节点>",
            "last_scene_beat": context.last_scene_beat.prompt(),
            "scene_blueprint": context.scene_blueprint.prompt(),
        }
