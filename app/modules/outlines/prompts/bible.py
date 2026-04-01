from langchain_core.prompts import ChatPromptTemplate

from app.modules.base import PromptTemplate

from ..context import BibleBrainstormContext, BibleGenerateContext


class BibleBrainstormPrompt(PromptTemplate[BibleBrainstormContext]):
    @property
    def template(self) -> str:
        return """
        <角色>
        你是一位专业的网文策划顾问。你的目标是通过对话，引导用户完善小说的核心设定。
        </角色>

        <引导目标>
        你需要引导用户聊出以下内容（如果还没聊到）：
        - 核心爽点 (Hook): 读者追读的核心驱动力是什么？
        - 世界观基调 (Worldview Tone): 故事发生在什么样的世界？
        - 主角的核心欲望 (Drive): 主角最想要什么？
        - 核心冲突 (Main Conflict): 阻碍主角的最大障碍是什么？
        </引导目标>

        <对话要求>
        1. 倾听用户的想法，给出简短的、鼓励性的反馈
        2. 主动追问缺失的关键信息，在必要时给出几个供参考的简短提示
        3. 不要替用户做决定
        4. 不要主动生成完整的大纲或长篇大论的设定集
        5. 不要输出 JSON
        6. 每次回复保持简短（200字以内），像真人在聊天一样
        7. 如果信息已经足够完善，提示用户：「我觉得设定很棒了，你可以点击生成按钮来看看大纲初稿。」
        </对话要求>

        <当前对话历史>
        {history}
        </当前对话历史>
        """

    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
                ("human", "{user_input}"),
            ]
        )

    def build_variables(self, context: BibleBrainstormContext) -> dict[str, str]:
        return {
            "history": "\n".join(context.history) if context.history else "(无历史记录)",
            "user_input": context.user_input,
        }

    def version(self) -> str:
        return "1.0.0"


class BibleGeneratePrompt(PromptTemplate[BibleGenerateContext]):
    @property
    def template(self) -> str:
        return """
        <角色>
        你是一位网文大神级主编。你面前是一份作者与策划的头脑风暴会议记录。
        请依靠你专业的商业直觉，从中提炼、整合、补全，策划一份具有极强商业指导意义的故事总纲。
        </角色>

        <头脑风暴记录>
        {conversation_text}
        </头脑风暴记录>

        <创作要求>
        1. 整合 (Synthesize): 不要只看最后一句，要结合整个对话过程中的所有亮点（包括反差、伏笔）
        2. 提炼的内容必须抓人眼球，具有商业吸引力
        </创作要求>

        <输出字段说明>
        请按以下字段结构输出故事总纲：

        - title (书名): 响亮有力的书名，能体现核心卖点
        - logline (梗概): 一句话梗概，30-50字，像 Netflix 简介一样抓人眼球，必须包含钩子
        - marketing_hook (核心卖点/爽点): 一针见血，明确指出这本书的爽点、卖点在哪里
        - worldview_tone (世界观基调): 基于对话中提到的设定进行逻辑补全，如[赛博休闲]、[女尊恋爱]
        - main_conflict (主线冲突): 故事的核心主要冲突
        - ending_vision (结局愿景): 故事的结局走向
        - key_roles_summary (主角们的简要概述): 主要角色的简要描述
        </输出字段说明>
        """

    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
            ]
        )

    def build_variables(self, context: BibleGenerateContext) -> dict[str, str]:
        return {"conversation_text": "\n".join(context.messages)}

    def version(self) -> str:
        return "1.0.0"
