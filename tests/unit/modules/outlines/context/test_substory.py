import pytest
from inline_snapshot import snapshot
from app.modules.outlines.context.substory import SubstoryBrainstormContext, SubstoryGenerateContext
from app.modules.outlines.schemas.bible import Bible
from app.modules.outlines.schemas.substory import (
    Substory,
    SubstoryActionNode,
    ChapterOriginalSubstoryNodes,
)
from app.modules.base.memory import ChapterSummary, CumulativeSubstorySummary
from app.modules.outlines.schemas.chapter import ChapterBlueprint, ChapterSceneBlueprint


@pytest.mark.unit()
def test_substory_brainstorm_context(
    history: list[str],
    user_input: str,
    bible: Bible,
) -> None:
    context = SubstoryBrainstormContext(
        bible=bible,
        history=history,
        user_input=user_input,
    )
    assert context.model_dump() == snapshot(
        {
            "history": ["test", "history"],
            "user_input": "test",
            "bible": {
                "title": "测试小说名",
                "logline": "这是一个测试用的核心梗概，描述了主角的冒险故事。",
                "marketing_hook": "无敌流，快节奏，系统文",
                "worldview_tone": "赛博朋克风格废土世界，基调灰暗但充满希望",
                "main_conflict": "底层平民与财阀高层的生存资源争夺战",
                "ending_vision": "主角推翻财阀，建立新的秩序",
                "key_roles_summary": "主角李四是孤儿，配角王五是他的黑客导师",
            },
        }
    )


@pytest.mark.unit()
def test_substory_generate_context(
    history: list[str],
    bible: Bible,
) -> None:
    context = SubstoryGenerateContext(
        bible=bible,
        history=history,
    )
    assert context.model_dump() == snapshot(
        {
            "history": ["test", "history"],
            "bible": {
                "title": "测试小说名",
                "logline": "这是一个测试用的核心梗概，描述了主角的冒险故事。",
                "marketing_hook": "无敌流，快节奏，系统文",
                "worldview_tone": "赛博朋克风格废土世界，基调灰暗但充满希望",
                "main_conflict": "底层平民与财阀高层的生存资源争夺战",
                "ending_vision": "主角推翻财阀，建立新的秩序",
                "key_roles_summary": "主角李四是孤儿，配角王五是他的黑客导师",
            },
        }
    )
