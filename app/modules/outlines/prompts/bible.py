from app.modules.base.prompt import PromptTemplate
from ..context.bible import BrainstormContext
from ..context.bible import BibleContext
from langchain_core.prompts import ChatPromptTemplate


class BrainstormPrompt(PromptTemplate[BrainstormContext]):
    @property
    def template(self) -> str:
        return """
        你是一位专业的网文策划顾问。你的目标是通过对话，引导用户完善小说的核心设定。
        
        【你的任务】
        1. 倾听用户的想法，给出简短的、鼓励性的反馈。
        2. **主动追问**缺失的关键信息，在必要时给出几个供参考的简短提示。你需要引导用户聊出以下内容（如果还没聊到）：
           - 核心爽点 (Hook)
           - 世界观基调 (Worldview Tone)
           - 主角的核心欲望 (Drive)
           - 核心冲突 (Main Conflict)
        
        【重要原则】
        - **不要** 替用户做决定。
        - **不要** 主动生成完整的大纲或长篇大论的设定集。
        - **不要** 输出 JSON。
        - 每次回复尽量保持简短（200字以内），像真人在聊天一样。
        - 如果你觉得信息已经足够完善了，可以提示用户：“我觉得设定很棒了，你可以点击生成按钮来看看大纲初稿。”

        【当前对话历史】
        {history}
        """

    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
                ("human", "{user_input}"),
            ]
        )

    def build_variables(self, context: BrainstormContext) -> dict[str, str]:
        return {
            "history": "\n".join(context.history)
            if context.history
            else "(无历史记录)",
            "user_input": context.user_input,
        }

    def version(self) -> str:
        return "1.0.0"


class BiblePrompt(PromptTemplate[BibleContext]):
    @property
    def template(self) -> str:
        return """
        你是一位网文大神级主编。
        你面前是一份**作者与策划的头脑风暴会议记录**。
        
        请仔细阅读这份记录，依靠你专业的商业直觉，从中提炼、整合、补全，策划一份具有极强商业指导意义的故事总纲。

        【头脑风暴记录】
        {conversation_text}

        【策划要求】
        1. **整合 (Synthesize)**: 不要只看最后一句，要结合整个对话过程中的所有亮点（包括反差、伏笔）。
        2. **Logline**: 提炼出一句话梗概，必须像 Netflix 简介一样抓人眼球。
        3. **Hook**: "marketing_hook" 必须一针见血，明确指出这本书的爽点、卖点在哪里。
        4. **Worldview_Tone**: 基于对话中提到的设定进行逻辑补全，确立世界观基调。
        5. **Main_Conflict**: 根据对话生成故事的核心主要冲突。
        6. **Ending_Vision**: 根据对话生成故事的结局愿景。
        7. **Key_Roles_Summary**: 主角们的简要概述。
        """

    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
            ]
        )

    def build_variables(self, context: BibleContext) -> dict[str, str]:
        return {"conversation_text": "\n".join(context.messages)}

    def version(self) -> str:
        return "1.0.0"
