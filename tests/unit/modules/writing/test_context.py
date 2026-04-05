import pytest
from inline_snapshot import snapshot

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


@pytest.mark.unit()
def test_chapter_scene_writing_context(
    bible: Bible,
    substory: Substory,
    chapter_original_substory_nodes: ChapterOriginalSubstoryNodes,
    chapter_blueprint: ChapterBlueprint,
    chapter_scene_blueprint: ChapterSceneBlueprint,
    chapter_scene: ChapterScene,
    cumulative_substory_summary: CumulativeSubstorySummary,
    chapter_summary: ChapterSummary,
    material_snippet: MaterialSnippet,
) -> None:
    context = ChapterSceneWritingContext(
        bible=bible,
        substory=substory,
        original_logic_nodes=chapter_original_substory_nodes,
        chapter_blueprint=chapter_blueprint,
        scene_blueprint=chapter_scene_blueprint,
        scene=chapter_scene,
        cumulative_substory_summary=cumulative_substory_summary,
        pre_chapter_summary=chapter_summary,
        previous_scene_chunk=SceneChunk(content="李四站在门前，犹豫了片刻。"),
        materials=[material_snippet],
    )
    assert context.model_dump() == snapshot(
        {
            "bible": {
                "title": "测试小说名",
                "logline": "这是一个测试用的核心梗概，描述了主角的冒险故事。",
                "marketing_hook": "无敌流，快节奏，系统文",
                "worldview_tone": "赛博朋克风格废土世界，基调灰暗但充满希望",
                "main_conflict": "底层平民与财阀高层的生存资源争夺战",
                "ending_vision": "主角推翻财阀，建立新的秩序",
                "key_roles_summary": "主角李四是孤儿，配角王五是他的黑客导师",
            },
            "substory": {
                "substory_title": "第一卷：初入废土",
                "logic_nodes": [
                    {
                        "cause": "黑帮抢夺贫民窟的净水装置",
                        "process": "主角为了保护妹妹被卷入冲突，意外接触到神秘源石",
                        "effect": "主角觉醒了雷电异能",
                        "exchange": "平静的生活被打破，被黑帮追杀",
                        "context": "此时全城的警方力量已被财阀抽走",
                    }
                ],
                "core_conflict": "主角能否在贫民窟的黑帮火拼中活下来",
                "status_change": "从手无寸铁的平民变为觉醒异能的战士",
            },
            "original_logic_nodes": {
                "nodes": [
                    {
                        "cause": "黑帮抢夺贫民窟的净水装置",
                        "process": "主角为了保护妹妹被卷入冲突，意外接触到神秘源石",
                        "effect": "主角觉醒了雷电异能",
                        "exchange": "平静的生活被打破，被黑帮追杀",
                        "context": "此时全城的警方力量已被财阀抽走",
                    }
                ]
            },
            "chapter_blueprint": {
                "chapter_index": 1,
                "title": "雨夜的枪声",
                "thematic_tone": "紧张、压抑",
                "opening_hook": "一颗子弹擦过李四的耳边，打碎了身后的净水器",
                "ending_cliffhanger": "李四倒在血泊中，眼看黑帮老大举起了枪，突然他的手心闪烁起蓝色的电光……",
                "scenes_blueprint": [
                    {
                        "location": "贫民窟的废弃工厂巷道",
                        "time_setting": "深夜，暴雨倾盆",
                        "characters": ["李四", "黑帮小喽啰", "妹妹小红"],
                        "objective": "李四试图带着妹妹逃离黑帮的包围圈",
                        "logic_bridge": "承接卷一节点1：黑帮火拼爆发",
                    }
                ],
            },
            "scene_blueprint": {
                "location": "贫民窟的废弃工厂巷道",
                "time_setting": "深夜，暴雨倾盆",
                "characters": ["李四", "黑帮小喽啰", "妹妹小红"],
                "objective": "李四试图带着妹妹逃离黑帮的包围圈",
                "logic_bridge": "承接卷一节点1：黑帮火拼爆发",
            },
            "scene": {
                "location": "贫民窟的废弃工厂巷道",
                "time_setting": "深夜，暴雨倾盆",
                "characters": ["李四", "黑帮小喽啰", "妹妹小红"],
                "objective": "李四试图带着妹妹逃离黑帮的包围圈",
                "logic_bridge": "承接卷一节点1：黑帮火拼爆发",
                "beats": [
                    {
                        "category": "动作",
                        "mood": "激昂",
                        "description": "李四翻滚躲开射击，同时抛出一枚自制电磁脉冲手雷",
                    }
                ],
            },
            "cumulative_substory_summary": {"summary": "黑帮大举搜索贫民窟，李四处于极度恐惧中。"},
            "pre_chapter_summary": {"summary": "上一章讲了李四逃入废弃工厂，暂时躲过了追捕。"},
            "previous_scene_chunk": {"content": "李四站在门前，犹豫了片刻。"},
            "materials": [
                {
                    "essential_text": "阴暗的走廊里弥漫着铁锈的味道。",
                    "category": "环境",
                    "mood": "压抑",
                    "tags": ["环境描写", "氛围感"],
                }
            ],
        }
    )


@pytest.mark.unit()
def test_chapter_writing_context(
    bible: Bible,
    substory: Substory,
    chapter_original_substory_nodes: ChapterOriginalSubstoryNodes,
    chapter_blueprint: ChapterBlueprint,
    chapter_outline: ChapterOutline,
    cumulative_substory_summary: CumulativeSubstorySummary,
    chapter_summary: ChapterSummary,
) -> None:
    context = ChapterWritingContext(
        bible=bible,
        substory=substory,
        original_logic_nodes=chapter_original_substory_nodes,
        chapter_blueprint=chapter_blueprint,
        chapter_outline=chapter_outline,
        cumulative_substory_summary=cumulative_substory_summary,
        pre_chapter_summary=chapter_summary,
        previous_scene_chunk=SceneChunk(content="这是上一章的结尾内容。"),
    )
    assert context.model_dump() == snapshot(
        {
            "bible": {
                "title": "测试小说名",
                "logline": "这是一个测试用的核心梗概，描述了主角的冒险故事。",
                "marketing_hook": "无敌流，快节奏，系统文",
                "worldview_tone": "赛博朋克风格废土世界，基调灰暗但充满希望",
                "main_conflict": "底层平民与财阀高层的生存资源争夺战",
                "ending_vision": "主角推翻财阀，建立新的秩序",
                "key_roles_summary": "主角李四是孤儿，配角王五是他的黑客导师",
            },
            "substory": {
                "substory_title": "第一卷：初入废土",
                "logic_nodes": [
                    {
                        "cause": "黑帮抢夺贫民窟的净水装置",
                        "process": "主角为了保护妹妹被卷入冲突，意外接触到神秘源石",
                        "effect": "主角觉醒了雷电异能",
                        "exchange": "平静的生活被打破，被黑帮追杀",
                        "context": "此时全城的警方力量已被财阀抽走",
                    }
                ],
                "core_conflict": "主角能否在贫民窟的黑帮火拼中活下来",
                "status_change": "从手无寸铁的平民变为觉醒异能的战士",
            },
            "original_logic_nodes": {
                "nodes": [
                    {
                        "cause": "黑帮抢夺贫民窟的净水装置",
                        "process": "主角为了保护妹妹被卷入冲突，意外接触到神秘源石",
                        "effect": "主角觉醒了雷电异能",
                        "exchange": "平静的生活被打破，被黑帮追杀",
                        "context": "此时全城的警方力量已被财阀抽走",
                    }
                ]
            },
            "chapter_blueprint": {
                "chapter_index": 1,
                "title": "雨夜的枪声",
                "thematic_tone": "紧张、压抑",
                "opening_hook": "一颗子弹擦过李四的耳边，打碎了身后的净水器",
                "ending_cliffhanger": "李四倒在血泊中，眼看黑帮老大举起了枪，突然他的手心闪烁起蓝色的电光……",
                "scenes_blueprint": [
                    {
                        "location": "贫民窟的废弃工厂巷道",
                        "time_setting": "深夜，暴雨倾盆",
                        "characters": ["李四", "黑帮小喽啰", "妹妹小红"],
                        "objective": "李四试图带着妹妹逃离黑帮的包围圈",
                        "logic_bridge": "承接卷一节点1：黑帮火拼爆发",
                    }
                ],
            },
            "chapter_outline": {
                "chapter_index": 1,
                "title": "雨夜的枪声",
                "thematic_tone": "紧张、压抑",
                "opening_hook": "一颗子弹擦过李四的耳边，打碎了身后的净水器",
                "ending_cliffhanger": "李四倒在血泊中，眼看黑帮老大举起了枪，突然他的手心闪烁起蓝色的电光……",
                "scenes": [
                    {
                        "location": "贫民窟的废弃工厂巷道",
                        "time_setting": "深夜，暴雨倾盆",
                        "characters": ["李四", "黑帮小喽啰", "妹妹小红"],
                        "objective": "李四试图带着妹妹逃离黑帮的包围圈",
                        "logic_bridge": "承接卷一节点1：黑帮火拼爆发",
                        "beats": [
                            {
                                "category": "动作",
                                "mood": "激昂",
                                "description": "李四翻滚躲开射击，同时抛出一枚自制电磁脉冲手雷",
                            }
                        ],
                    }
                ],
            },
            "cumulative_substory_summary": {"summary": "黑帮大举搜索贫民窟，李四处于极度恐惧中。"},
            "pre_chapter_summary": {"summary": "上一章讲了李四逃入废弃工厂，暂时躲过了追捕。"},
            "previous_scene_chunk": {"content": "这是上一章的结尾内容。"},
        }
    )
