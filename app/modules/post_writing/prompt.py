from langchain_core.prompts import ChatPromptTemplate

from app.modules.base.prompt import PromptTemplate

from .context import ChapterSummaryContext, SubstoryCumulativeSummaryContext


class ChapterSummaryPrompt(PromptTemplate[ChapterSummaryContext]):
    @property
    def template(self) -> str:
        return """
        <角色>
        你是一位专业的小说编辑，擅长提炼章节核心内容，能够准确把握剧情脉络和人物发展。你的总结简洁精准，能够为后续创作提供清晰的上下文参考。
        </角色>

        <全局背景>
        {overview_outline}

        {substory_outline}
        </全局背景>

        <章节规划参考>
        {original_logic_nodes}

        {chapter_outline}
        </章节规划参考>

        <剧情上下文>
        {cumulative_substory_summary}

        {pre_chapter_summary}
        </剧情上下文>

        <待总结的章节内容>
        {chapter_content}
        </待总结的章节内容>

        <任务要求>
        请根据上述章节内容，生成一份简洁的章节总结，需满足以下要求：

        1. **核心事件**：提炼本章发生的主要事件和关键情节转折点。
        2. **人物动态**：记录主要人物的行动、决策及其心理变化。
        3. **剧情推进**：说明本章在整体故事线中的推进作用，与卷钢逻辑节点的对应关系。
        4. **状态更新**：记录任何重要的状态变化（如人物关系、势力格局、物品获取等）。
        5. **格式要求**：总结控制在200-400字，分点列出，便于快速阅读。
        </任务要求>
        """

    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
            ]
        )

    def build_variables(self, context: ChapterSummaryContext) -> dict[str, str]:
        original_logic_nodes_prompt = f"""<章节对应卷钢节点>\n{
            "\n".join([node.prompt() for node in context.original_logic_nodes])
        }\n</章节对应卷钢节点>"""
        return {
            "overview_outline": context.bible.prompt(),
            "substory_outline": context.substory.prompt(),
            "original_logic_nodes": original_logic_nodes_prompt,
            "chapter_outline": context.chapter_outline.prompt(),
            "cumulative_substory_summary": f"<卷内进度总结>\n{context.cumulative_substory_summary}\n</卷内进度总结>",
            "pre_chapter_summary": f"<上一章节总结>\n{context.pre_chapter_summary}\n</上一章节总结>",
            "chapter_content": context.chapter.prompt(),
        }

    def version(self) -> str:
        return "1.0.0"


class SubstoryCumulativeSummaryPrompt(PromptTemplate[SubstoryCumulativeSummaryContext]):
    @property
    def template(self) -> str:
        return """
        <角色>
        你是一位专业的小说编辑，负责维护故事进度的累积总结。你能够将新章节的内容有机融入现有总结，保持信息的连贯性和完整性。
        </角色>

        <全局背景>
        {overview_outline}

        {substory_outline}
        </全局背景>

        <当前卷内累积总结>
        {cumulative_substory_summary}
        </当前卷内累积总结>

        <新完成的章节总结>
        {current_chapter_summary}
        </新完成的章节总结>

        <任务要求>
        请将新完成的章节总结融入到当前卷内累积总结中，生成更新后的累积总结，需满足以下要求：

        1. **信息整合**：将新章节的关键信息有机融入现有总结，避免简单堆叠。
        2. **时序清晰**：保持事件发展的时间线清晰，体现剧情的递进关系。
        3. **重点突出**：突出对后续创作有参考价值的信息（如人物状态、关系变化、悬念铺设等）。
        4. **冗余删除**：删除已过时或不再重要的细节，保持总结精炼。
        5. **格式要求**：更新后的总结控制在300-600字，保持结构清晰。
        </任务要求>
        """

    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
            ]
        )

    def build_variables(self, context: SubstoryCumulativeSummaryContext) -> dict[str, str]:
        return {
            "overview_outline": context.bible.prompt(),
            "substory_outline": context.substory.prompt(),
            "cumulative_substory_summary": f"<卷内进度总结>\n{context.cumulative_substory_summary}\n</卷内进度总结>",
            "current_chapter_summary": f"<当前章节总结>\n{context.current_chapter_summary}\n</当前章节总结>",
        }

    def version(self) -> str:
        return "1.0.0"
