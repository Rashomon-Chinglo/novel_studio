import pytest
from inline_snapshot import snapshot

from app.modules.materials.schemas import ExtractedResult, MaterialSnippet


@pytest.mark.unit()
def test_material_snippet_valid_data():
    snippet = MaterialSnippet(
        essential_text="窗外下着大雨，雷声阵阵。",
        category="环境",
        mood="压抑",
        tags=["天气", "开场"],
    )
    assert snippet.model_dump() == snapshot(
        {
            "essential_text": "窗外下着大雨，雷声阵阵。",
            "category": "环境",
            "mood": "压抑",
            "tags": ["天气", "开场"],
        }
    )


@pytest.mark.unit()
def test_material_snippet_prompt():
    snippet = MaterialSnippet(
        essential_text="窗外下着大雨，雷声阵阵。",
        category="环境",
        mood="压抑",
        tags=["天气", "开场"],
    )
    assert snippet.prompt(1) == snapshot("""\
<参考素材1>
- **文本**: 窗外下着大雨，雷声阵阵。
- **描写技法**: 环境
- **情绪**: 压抑
- **内容标签**: 天气, 开场
</参考素材1>\
""")


@pytest.mark.unit()
def test_material_snippet_prompt_no_index():
    snippet = MaterialSnippet(
        essential_text="窗外下着大雨，雷声阵阵。",
        category="环境",
        mood="压抑",
        tags=["天气", "开场"],
    )
    assert snippet.prompt() == snapshot("""\
<参考素材>
- **文本**: 窗外下着大雨，雷声阵阵。
- **描写技法**: 环境
- **情绪**: 压抑
- **内容标签**: 天气, 开场
</参考素材>\
""")


@pytest.mark.unit()
def test_material_result_valid_data():
    result = ExtractedResult(
        snippets=[
            MaterialSnippet(
                essential_text="窗外下着大雨，雷声阵阵。",
                category="环境",
                mood="压抑",
                tags=["天气", "开场"],
            ),
            MaterialSnippet(
                essential_text="他紧握着拳头，指关节微微发白。",
                category="动作",
                mood="愤怒",
                tags=["肢体动作"],
            ),
        ]
    )
    assert result.model_dump() == snapshot(
        {
            "snippets": [
                {
                    "essential_text": "窗外下着大雨，雷声阵阵。",
                    "category": "环境",
                    "mood": "压抑",
                    "tags": ["天气", "开场"],
                },
                {
                    "essential_text": "他紧握着拳头，指关节微微发白。",
                    "category": "动作",
                    "mood": "愤怒",
                    "tags": ["肢体动作"],
                },
            ]
        }
    )
