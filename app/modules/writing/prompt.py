from langchain_core.prompts import ChatPromptTemplate

from app.modules.base import PromptTemplate

from .context import ChapterSceneWritingContext


class ChapterSceneWritingPrompt(PromptTemplate[ChapterSceneWritingContext]):
    @property
    def template(self) -> str:
        return """
        <角色>
        你是一位拥有丰富创作经验的网文作家，擅长细腻的情感描写和紧张的剧情推进。你的文笔流畅自然，画面感强，能够让读者身临其境。
        </角色>

        <全局背景>
        {overview_outline}

        {substory_outline}
        </全局背景>

        {reference_texts}

        <剧情上下文>
        {cumulative_substory_summary}

        {pre_chapter_summary}

        {previous_content}
        </剧情上下文>

        <本章规划>
        {original_logic_nodes}

        {chapter_blueprint}
        </本章规划>

        <本场戏设定>
        {scene_blueprint}
        </本场戏设定>

        <场景节拍>
        以下是本场戏需要扩写的内容大纲（场景节拍）：
        {scene}
        </场景节拍>

        <创作要求>
        请根据上述「场景节拍」，进行正文创作，需满足以下要求：

        1. **严格遵循节拍**：请严格按照「场景节拍」中规划的动作、对话和心理活动进行描写，不要随意更改剧情走向或增加无关情节。
        2. **注重画面感**：多使用感官描写（视觉、听觉、嗅觉等）来构建场景，避免干瘪的陈述。
        3. **人物贴合**：人物的台词和行动必须符合其性格设定（参考全局背景），保持语气和行为的一致性。
        4. **代入感**：注重氛围营造，让读者能够感受到场景中的情绪流动（如紧张、温馨、压抑等）。
        5. **格式**：直接输出小说正文内容，无需包含任何解释性文字或标题。
        </创作要求>
        """

    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
            ]
        )

    def build_variables(self, context: ChapterSceneWritingContext) -> dict[str, str]:
        materials_prompt = "\n".join(
            [material.prompt(index + 1) for index, material in enumerate(context.materials)]
        )

        return {
            "overview_outline": context.bible.prompt(),
            "substory_outline": context.substory.prompt(),
            "original_logic_nodes": context.original_logic_nodes.prompt(),
            "chapter_blueprint": context.chapter_blueprint.prompt(),
            "scene_blueprint": context.scene_blueprint.prompt(),
            "scene": context.scene.prompt(),
            "cumulative_substory_summary": context.cumulative_substory_summary.prompt(),
            "pre_chapter_summary": context.pre_chapter_summary.prompt(),
            "previous_content": f"<上文内容>\n{context.previous_content}\n</上文内容>",
            "reference_texts": f"<参考素材>\n{materials_prompt}\n</参考素材>",
        }

    def version(self) -> str:
        return "1.0.0"
