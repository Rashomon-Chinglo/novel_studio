from app.modules.base.prompt import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from ..context.chapter import ChapterBlueprintContext
from ..context.chapter import ChapterBlueprintBrainstormContext
from ..context.chapter import ChapterSceneContext


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
        return {
            "overview_outline": context.bible.prompt(),
            "substory_outline": context.substory.prompt(),
            "cumulative_substory_summary": f"<卷内进度>\n{context.cumulative_substory_summary}\n</卷内进度>",
            "pre_chapter_summary": f"<上章总结>\n{context.pre_chapter_summary}\n</上章总结>",
            "logic_nodes_to_process": f"<逻辑节点>\n{'\n'.join([node.prompt() for node in context.logic_nodes_to_process])}\n</逻辑节点>",
        }


class BlueprintBrainstormPrompt(PromptTemplate[ChapterBlueprintBrainstormContext]):
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
                ("human", "请根据我们的讨论，重新生成这一章的 Blueprint。"),
            ]
        )

    def build_variables(
        self, context: ChapterBlueprintBrainstormContext
    ) -> dict[str, str]:
        return {
            "overview_outline": context.bible.prompt(),
            "substory_outline": context.substory.prompt(),
            "chapter_blueprint": context.chapter_blueprint.prompt(),
            "cumulative_substory_summary": f"<卷内进度>\n{context.cumulative_substory_summary}\n</卷内进度>",
            "pre_chapter_summary": f"<上章总结>\n{context.pre_chapter_summary}\n</上章总结>",
            "logic_nodes_to_process": f"<逻辑节点>\n{context.format_logic_nodes_to_process()}\n</逻辑节点>",
            "conversation_history": f"<头脑风暴记录>\n{context.format_conversation_history()}\n</头脑风暴记录>",
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
        return {
            "overview_outline": context.bible.prompt(),
            "substory_outline": context.substory.prompt(),
            "chapter_blueprint": context.chapter_blueprint.prompt(),
            "cumulative_substory_summary": f"<卷内进度>\n{context.cumulative_substory_summary}\n</卷内进度>",
            "pre_chapter_summary": f"<上章总结>\n{context.pre_chapter_summary}\n</上章总结>",
            "logic_nodes_to_process": f"<逻辑节点>\n{context.format_logic_nodes_to_process()}\n</逻辑节点>",
            "last_scene_beat": context.last_scene_beat.prompt(),
            "scene_blueprint": context.scene_blueprint.prompt(),
        }
