import pytest

from app.modules.materials.context import MaterialsMiningContext
from inline_snapshot import snapshot


@pytest.mark.unit()
def test_material_context() -> None:
    context = MaterialsMiningContext(text="这是一个测试文本。")
    assert context.model_dump() == snapshot({"text": "这是一个测试文本。"})
