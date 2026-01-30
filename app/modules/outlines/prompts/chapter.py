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
        <角色>
        你是一位拥有深厚编剧功底的网文大纲架构师。你擅长将抽象的因果逻辑转化为具备画面感和节奏感的场景序列。
        </角色>

        <全局背景>
        {overview_outline}

        {substory_outline}
        </全局背景>

        <本章上下文>
        {cumulative_substory_summary}

        {pre_chapter_summary}

        {logic_nodes_to_process}
        </本章上下文>

        <创作要求>
        请根据上述「本章逻辑节点」，结合全局背景，规划本章节的「场景骨架」，需满足以下要求：

        1. 场景划分原则
           - 场景转换：地点、时间或核心人物组合变化时需划分新场景
           - 场景数量：根据逻辑节点复杂度合理控制，通常 2-5 个场景为宜
           - 每个场景需有明确的戏剧目标

        2. 节奏把控
           - 开篇：快速切入，建立本章基调或承接上章悬念
           - 中段：交替安排张弛节奏，推进核心矛盾
           - 结尾：设置钩子或情绪高点，吸引继续阅读

        3. 逻辑一致性
           - 确保所有逻辑节点在场景骨架中有所体现
           - 人物行为需符合其既定动机和性格
        </创作要求>

        <输出字段说明>
        请按以下字段结构输出章节蓝图：

        - chapter_index (章节序号): 从1开始的整数
        - title (章节标题): 简洁有力，4-10字，需体现本章核心事件或情绪
        - thematic_tone (章节主题色调): 描述本章情绪走向，如"压抑→爆发"、"悬疑→揭晓"
        - opening_hook (章节开头的悬念): 本章开篇如何抓住读者，可为空
        - ending_cliffhanger (章节结尾的悬念): 结尾留下的钩子，吸引继续阅读，可为空
        - scenes_blueprint (序列场景蓝图): 场景数组，每个场景包含：
          - location (场景地点): 具体地点名称
          - time_setting (场景时间及环境): 时间点及环境氛围描述
          - characters (场景中的人物): 本场景出场人物列表
          - objective (本场戏的目标): 本场景需要达成的戏剧目标
          - logic_bridge (逻辑桥接): 明确指出承接的卷纲逻辑节点
        </输出字段说明>
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
        <角色>
        你是一位拥有深厚编剧功底的网文大纲架构师，同时也是一位善于倾听的创意伙伴。
        你的目标是通过对话引导用户完善本章节的蓝图，激发他们的创意灵感。
        </角色>

        <全局背景>
        {overview_outline}

        {substory_outline}
        </全局背景>

        <本章上下文>
        {cumulative_substory_summary}

        {pre_chapter_summary}

        {logic_nodes_to_process}
        </本章上下文>

        <当前蓝图初稿>
        {chapter_blueprint}
        </当前蓝图初稿>

        <对话要求>
        作为创意伙伴，请遵循以下原则：

        1. 倾听与反馈
           - 认真倾听用户的想法，给出简短、鼓励性的反馈
           - 肯定用户创意中的亮点，指出其与人设/剧情的契合之处

        2. 引导与追问
           - 主动询问用户对当前蓝图是否满意，有无需要调整的地方
           - 针对模糊或薄弱的部分，提出具体的引导性问题

        3. 建议与启发
           - 在用户需要时，提供 2-3 个简短的创意方向供参考
           - 建议应基于全局背景和本章上下文，避免脱离设定

        4. 收尾判断
           - 当蓝图已足够完善时，提示用户：「我觉得设定很棒了，你可以点击生成本章初稿了。」
        </对话要求>
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
        <角色>
        你是一位拥有深厚编剧功底的网文场景设计师。你擅长将场景蓝图转化为具有画面感、节奏感和情感张力的场景节拍序列。
        </角色>

        <全局背景>
        {overview_outline}

        {substory_outline}
        </全局背景>

        <本章上下文>
        {chapter_blueprint}

        {logic_nodes_to_process}

        {cumulative_substory_summary}

        {pre_chapter_summary}
        </本章上下文>

        <本场景任务>
        {last_scene_beat}

        {scene_blueprint}
        </本场景任务>

        <创作要求>
        请为上述「场景蓝图」设计详细的「场景节拍序列」，需满足以下要求：

        1. 节拍设计原则
           - 动作具象：每个节拍应包含具体的人物动作、对话或心理变化，而非抽象描述
           - 因果推进：节拍之间应有明确的因果逻辑，推动剧情向场景目标演进
           - 节奏把控：根据场景类型调整节奏——冲突场景紧凑有力，情感场景留有余韵

        2. 衔接要求
           - 承上：首个节拍需自然衔接「上一场景的结束节拍」，保持情绪和动作的连贯性
           - 启下：最后一个节拍应为下一场景留下过渡空间或悬念钩子

        3. 逻辑一致性
           - 确保场景内容与「本章逻辑节点」保持一致
           - 人物行为需符合「全局背景」中的人设和动机
        </创作要求>

        <输出字段说明>
        请在「场景蓝图」基础上，补充「场景节拍序列」，输出完整的场景结构：

        - location (场景地点): 保持与输入的场景蓝图一致
        - time_setting (场景时间及环境): 保持与输入的场景蓝图一致
        - characters (场景中的人物): 保持与输入的场景蓝图一致
        - objective (本场戏的目标): 保持与输入的场景蓝图一致
        - logic_bridge (逻辑桥接): 保持与输入的场景蓝图一致
        - beats (场景内的动作节拍序列): 节拍数组，每个节拍包含：
          - type (场景类型): 节拍类型，如"对话"、"动作"、"心理"、"环境描写"等
          - description (具体的剧情动作点): 具体发生了什么，需包含人物、动作、目的，约50-100字
        </输出字段说明>
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
        last_scene_beat = (
            context.last_scene_beat.prompt()
            if context.last_scene_beat
            else "<上一场景结束节拍>无（本章第一场景）</上一场景结束节拍>"
        )
        return {
            "overview_outline": context.bible.prompt(),
            "substory_outline": context.substory.prompt(),
            "chapter_blueprint": context.chapter_blueprint.prompt(),
            "cumulative_substory_summary": f"<卷内进度>\n{context.cumulative_substory_summary}\n</卷内进度>",
            "pre_chapter_summary": f"<上章总结>\n{context.pre_chapter_summary}\n</上章总结>",
            "logic_nodes_to_process": f"<本章逻辑节点>\n{logic_nodes_to_process}\n</本章逻辑节点>",
            "last_scene_beat": last_scene_beat,
            "scene_blueprint": context.scene_blueprint.prompt(),
        }
