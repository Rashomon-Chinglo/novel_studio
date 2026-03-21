import pytest
from inline_snapshot import snapshot
from pytest_mock import MockerFixture

from app.modules.materials.engine import MaterialEngine
from app.modules.materials.schemas import ExtractedResult, MaterialSnippet
from tests.support.llm import EngineContext, FakeLLM, FakeLLMFactory


@pytest.fixture()
def engine_context(
    mocker: MockerFixture, fake_llm_factory: FakeLLMFactory
) -> EngineContext[MaterialEngine, ExtractedResult]:
    fake_llm: FakeLLM[ExtractedResult] = fake_llm_factory(
        text_responses=[""],
        structured_responses=[
            ExtractedResult(
                snippets=[
                    MaterialSnippet(
                        essential_text="现代化 Mock 提取的内容",
                        category="心理",
                        mood="愤怒",
                        tags=["pytest-mock"],
                    )
                ]
            )
        ],
    )
    mocker.patch("app.modules.materials.chain.get_llm", return_value=fake_llm)
    return EngineContext(engine=MaterialEngine(), fake_llm=fake_llm)


@pytest.mark.unit()
@pytest.mark.parametrize(
    ("text", "length_of_chunks"),
    [
        ("", 0),
        ("你好，你今天晚上吃什么？", 1),
        ("你好，你今天晚上吃什么？" * 50, 2),
    ],
)
def test_engine_split_text(
    engine_context: EngineContext[MaterialEngine, ExtractedResult], text: str, length_of_chunks: int
) -> None:
    chunks = engine_context.engine.split_text(text)
    assert len(chunks) == length_of_chunks


@pytest.mark.unit()
@pytest.mark.asyncio()
async def test_engine_mine(engine_context: EngineContext[MaterialEngine, ExtractedResult]) -> None:
    engine = engine_context.engine
    fake_llm = engine_context.fake_llm

    mock_response = ExtractedResult(
        snippets=[
            MaterialSnippet(
                essential_text="现代化 Mock 提取的内容",
                category="心理",
                mood="愤怒",
                tags=["pytest-mock"],
            )
        ]
    )

    context = MaterialEngine.MaterialsMiningContext(text="test")
    result = await engine.mine(context)

    assert result == mock_response

    # Assert get_llm was used to create structured output
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
