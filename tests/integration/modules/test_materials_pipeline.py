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
from tests.support.llm import EngineContext, FakeLLMFactory

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
def material_engine_context(
    mocker: MockerFixture,
    extracted_result: ExtractedResult,
    fake_llm_factory: FakeLLMFactory,
) -> EngineContext[MaterialEngine, ExtractedResult]:
    fake_llm = fake_llm_factory(structured_responses=[extracted_result])
    mocker.patch("app.modules.materials.chain.get_llm", return_value=fake_llm)
    return EngineContext(engine=MaterialEngine(), fake_llm=fake_llm)


@pytest.mark.integration()
@pytest.mark.asyncio()
async def test_pipeline(
    original_text: str,
    material_engine_context: EngineContext[MaterialEngine, ExtractedResult],
    extracted_result: ExtractedResult,
):
    material_engine = material_engine_context.engine
    fake_llm = material_engine_context.fake_llm
    snippets = material_engine.split_text(original_text)
    snippet = snippets[0]
    result = await material_engine.mine(MaterialsMiningContext(text=snippet))
    assert len(snippets) == snapshot(6)
    assert len(snippet) == snapshot(424)
    assert result == extracted_result
    assert fake_llm.structured_output_requests == snapshot(
        [
            {
                "schema": ExtractedResult,
                "include_raw": False,
                "method": "function_calling",
                "strict": True,
            }
        ]
    )
    assert fake_llm.structured_responses == snapshot(
        [
            ExtractedResult(
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
        ]
    )
