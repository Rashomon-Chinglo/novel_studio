import pytest

from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.materials.schemas import MaterialSnippet
from app.modules.outlines.schemas.bible import Bible
from app.modules.outlines.schemas.chapter import (
    ChapterBlueprint,
    ChapterOutline,
    ChapterScene,
    ChapterSceneBlueprint,
)
from app.modules.outlines.schemas.substory import ChapterOriginalSubstoryNodes, Substory
from app.modules.writing.context import ChapterSceneWritingContext, ChapterWritingContext
from app.modules.writing.schemas import SceneChunk


@pytest.fixture()
def scene_chunk() -> SceneChunk:
    return SceneChunk(content="李四深吸一口气，推开了沉重的铁门。")


@pytest.fixture()
def chapter_scene_writing_context(
    bible: Bible,
    substory: Substory,
    chapter_original_substory_nodes: ChapterOriginalSubstoryNodes,
    chapter_blueprint: ChapterBlueprint,
    chapter_scene_blueprint: ChapterSceneBlueprint,
    chapter_scene: ChapterScene,
    cumulative_substory_summary: CumulativeSubstorySummary,
    chapter_summary: ChapterSummary,
    material_snippet: MaterialSnippet,
) -> ChapterSceneWritingContext:
    return ChapterSceneWritingContext(
        bible=bible,
        substory=substory,
        original_logic_nodes=chapter_original_substory_nodes,
        chapter_blueprint=chapter_blueprint,
        scene_blueprint=chapter_scene_blueprint,
        scene=chapter_scene,
        cumulative_substory_summary=cumulative_substory_summary,
        pre_chapter_summary=chapter_summary,
        previous_content="李四站在门前，犹豫了片刻。",
        materials=[material_snippet],
    )


@pytest.fixture()
def chapter_writing_context(
    bible: Bible,
    substory: Substory,
    chapter_original_substory_nodes: ChapterOriginalSubstoryNodes,
    chapter_blueprint: ChapterBlueprint,
    chapter_outline: ChapterOutline,
    cumulative_substory_summary: CumulativeSubstorySummary,
    chapter_summary: ChapterSummary,
) -> ChapterWritingContext:
    return ChapterWritingContext(
        bible=bible,
        substory=substory,
        original_logic_nodes=chapter_original_substory_nodes,
        chapter_blueprint=chapter_blueprint,
        chapter_outline=chapter_outline,
        cumulative_substory_summary=cumulative_substory_summary,
        pre_chapter_summary=chapter_summary,
        previous_content="这是上一章的结尾内容。",
    )
