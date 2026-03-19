from pathlib import Path

import pytest
from inline_snapshot import snapshot
from pytest_mock import MockerFixture

from app.modules.materials.context import MaterialsMiningContext
from app.modules.materials.engine import MaterialEngine
from app.modules.materials.schemas import (
    ExtractedResult,
    MaterialSnippet,
)

FIXTURES_DIR = Path(__file__).parent.parent.parent / "fixtures"


@pytest.fixture()
def original_text():
    text = (FIXTURES_DIR / "test_chapter_1.txt").read_text(encoding="utf-8")
    return text


@pytest.fixture()
def extracted_result() -> ExtractedResult:
    return ExtractedResult(
        snippets=[
            MaterialSnippet(
                essential_text="他猛地一拍桌子，怒吼道：‘不可能！’",
                category="动作",
                mood="激昂",
                tags=["动作", "情绪"],
            ),
            MaterialSnippet(
                essential_text="夕阳的余晖洒在湖面上，泛起粼粼金光，微风拂过，带来阵阵清凉。",
                category="环境",
                mood="平静",
                tags=["平静", "环境"],
            ),
        ]
    )


@pytest.fixture()
def material_engine(mocker: MockerFixture, extracted_result: ExtractedResult):
    mining_chain = mocker.patch("app.modules.materials.engine.get_mining_chain")
    mining_chain.return_value.ainvoke = mocker.AsyncMock(return_value=extracted_result)
    return MaterialEngine()


@pytest.mark.integration()
@pytest.mark.asyncio()
async def test_pipeline(
    original_text: str, material_engine: MaterialEngine, extracted_result: ExtractedResult
):
    snippets = material_engine.split_text(original_text)
    snippet = snippets[0]
    assert len(snippets) == snapshot(6)
    assert len(snippet) == snapshot(424)
    result = await material_engine.mine(MaterialsMiningContext(text=snippet))
    assert result == extracted_result
