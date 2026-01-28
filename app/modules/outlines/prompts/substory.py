from langchain_core.prompts import ChatPromptTemplate

from app.modules.base.prompt import PromptTemplate

from ..context.substory import SubstoryBrainstormContext, SubstoryGenerateContext


class SubstoryBrainstormPrompt(PromptTemplate[SubstoryBrainstormContext]):
    @property
    def template(self) -> str:
        return """
        你是一位精通故事结构的剧情架构师。你的目标是协助作者策划小说中的一个具体篇章（分卷/副本/Substory）。

        【你的任务】
        1. 倾听作者的想法，给出简短、有建设性的反馈。
        2. **主动追问**缺失的关键剧情逻辑，引导用户聊出以下内容：
           - **本卷核心冲突** (Core Conflict): 这一卷主要解决什么问题？对抗什么？
           - **起止状态变化** (Status Change): 这一卷开始和结束时，主角或世界有什么本质的不同？
           - **关键因果链** (Logic Chain): 大致的剧情走向，A导致B，B导致C的逻辑链条。

        【重要原则】
        - 始终基于“因果逻辑”来审视剧情，如果发现逻辑断层，请温和地指出来。
        - **不要** 替用户做决定。
        - **不要** 主动生成完整的JSON或长篇大论。
        - 每次回复尽量保持简短（200字以内），像真人在聊天一样。
        - 如果你觉得剧情逻辑已经通顺，可以提示用户：“我觉得这一卷的逻辑链很清晰了，可以点击生成按钮来查看分卷大纲。”

        {overview_outline}

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

    def build_variables(self, context: SubstoryBrainstormContext) -> dict[str, str]:
        return {
            "history": "\n".join(context.history) if context.history else "(无历史记录)",
            "user_input": context.user_input,
            "overview_outline": context.bible.prompt(),
        }

    def version(self) -> str:
        return "1.0.0"


class SubstoryGeneratePrompt(PromptTemplate[SubstoryGenerateContext]):
    @property
    def template(self) -> str:
        return """
            你是一位资深网文主编，擅长梳理严密的剧情逻辑。
            你面前是关于小说某一分卷（Substory）的**头脑风暴会议记录**，以及该书的**总纲（Bible）**。

            请依据这些信息，策划出该分卷的详细结构大纲。

            {overview_outline}

            【分卷头脑风暴记录】
            {conversation_text}

            【策划要求】
            1. **承上启下**: 确保分卷剧情符合总纲的世界观、人物设定和整体基调。
            2. **逻辑严密 (Logic Nodes)**: 剧情必须由因果驱动，而非巧合。请构建一组 `SubstoryActionNode`，清楚地描述：
            - **Cause (起因)**: 触发事件。
            - **Process (经过)**: 冲突与行动。
            - **Effect (结果)**: 直接后果。
            - **Exchange (价值升降)**: 这一环节中发生的价值极性变化（如：安全->危险，爱->恨，无知->顿悟）。
            3. **Core Conflict**: 提炼本卷最核心的矛盾冲突。
            4. **Status Change**: 明确本卷结束时，相对于开始时产生的不可逆转的状态改变。
            """

    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
            ]
        )

    def build_variables(self, context: SubstoryGenerateContext) -> dict[str, str]:
        return {
            "overview_outline": context.bible.prompt(),
            "conversation_text": "\n".join(context.history),
        }

    def version(self) -> str:
        return "1.0.0"
