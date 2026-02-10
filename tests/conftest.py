"""
Pytest 全局配置和 Fixtures

这个文件包含了所有测试共享的 fixtures 和配置。
遵循现代 pytest 最佳实践，使用类型注解和清晰的文档字符串。
"""

import os
from collections.abc import AsyncGenerator, Generator
from typing import Any
from unittest.mock import AsyncMock, MagicMock

# ============================================================================
# 测试环境初始化：必须在导入任何 app 代码之前
# ============================================================================
os.environ["OPENAI_API_KEY"] = "sk-mock-key"
os.environ["JINA_API_KEY"] = "jina-mock-key"

import pytest
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from app.modules.materials.context import MaterialsMiningContext
from app.modules.materials.schemas import ExtractedResult, MaterialSnippet


# ============================================================================
# 测试数据 Fixtures
# ============================================================================


@pytest.fixture
def sample_novel_text() -> str:
    """提供示例小说文本用于测试"""
    return """
    夜幕降临，城市的霓虹灯开始闪烁。李明站在天台边缘，望着脚下车水马龙的街道。
    
    "你真的要这么做吗？"身后传来熟悉的声音。
    
    他没有回头，只是轻声说："我已经没有选择了。"风吹乱了他的头发，眼神中透着坚定与无奈。
    
    这座城市太大了，大到可以容纳所有人的梦想，却容不下一个普通人的真心。
    """


@pytest.fixture
def sample_material_snippet() -> MaterialSnippet:
    """提供示例素材片段"""
    return MaterialSnippet(
        essential_text="风吹乱了他的头发，眼神中透着坚定与无奈。",
        category="外貌",
        mood="压抑",
        tags=["都市", "告别", "成长"],
    )


@pytest.fixture
def sample_extracted_result(
    sample_material_snippet: MaterialSnippet,
) -> ExtractedResult:
    """提供示例提取结果"""
    return ExtractedResult(snippets=[sample_material_snippet])


@pytest.fixture
def sample_mining_context(sample_novel_text: str) -> MaterialsMiningContext:
    """提供示例挖掘上下文"""
    return MaterialsMiningContext(text=sample_novel_text)


# ============================================================================
# Mock LLM Fixtures
# ============================================================================


class MockChatModel(BaseChatModel):
    """Mock LangChain ChatModel 用于测试

    这是一个完整的 Mock 实现，避免真实 LLM 调用。
    支持自定义响应内容和异步调用。
    """

    mock_response: dict[str, Any]

    def __init__(self, mock_response: dict[str, Any] | None = None, **kwargs: Any):
        super().__init__(**kwargs)
        self.mock_response = mock_response or {}

    @property
    def _llm_type(self) -> str:
        return "mock"

    def _generate(
        self,
        messages: list,
        stop: list[str] | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        """同步生成（不推荐使用，仅为兼容性）"""
        message = AIMessage(content=str(self.mock_response))
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    async def _agenerate(
        self,
        messages: list,
        stop: list[str] | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        """异步生成（推荐使用）"""
        message = AIMessage(content=str(self.mock_response))
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])


@pytest.fixture
def mock_llm_response(sample_extracted_result: ExtractedResult) -> dict[str, Any]:
    """Mock LLM 响应数据"""
    return sample_extracted_result.model_dump()


@pytest.fixture
def mock_chat_model(mock_llm_response: dict[str, Any]) -> MockChatModel:
    """提供 Mock ChatModel"""
    return MockChatModel(mock_response=mock_llm_response)


@pytest.fixture
def mock_llm_chain(mock_llm_response: dict[str, Any]) -> MagicMock:
    """提供 Mock LangChain Chain

    这个 fixture 模拟了 LangChain 的 chain.ainvoke() 调用。
    返回预定义的响应，避免真实 API 调用。
    """
    chain = MagicMock()
    chain.ainvoke = AsyncMock(return_value=mock_llm_response)
    return chain


# ============================================================================
# 数据库 Fixtures (预留)
# ============================================================================


@pytest.fixture
async def async_db_session() -> AsyncGenerator[Any, None]:
    """提供异步数据库会话（预留）

    TODO: 实现真实的测试数据库会话
    目前返回 Mock 对象
    """
    session = MagicMock()
    try:
        yield session
    finally:
        await session.close() if hasattr(session, "close") else None


# ============================================================================
# 向量存储 Fixtures (预留)
# ============================================================================


@pytest.fixture
def mock_vector_store() -> MagicMock:
    """提供 Mock 向量存储（预留）

    TODO: 实现真实的 ChromaDB 测试实例
    """
    store = MagicMock()
    store.add_texts = AsyncMock(return_value=["id1", "id2"])
    store.similarity_search = AsyncMock(return_value=[])
    return store


# ============================================================================
# Pytest 配置钩子
# ============================================================================


def pytest_configure(config: pytest.Config) -> None:
    """Pytest 配置钩子

    在测试运行前执行，用于注册自定义标记等。
    """
    config.addinivalue_line("markers", "unit: 单元测试标记")
    config.addinivalue_line("markers", "integration: 集成测试标记")
    config.addinivalue_line("markers", "slow: 慢速测试标记")
    config.addinivalue_line("markers", "llm: 需要真实 LLM 调用的测试")
    config.addinivalue_line("markers", "bdd: BDD 测试标记")


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """修改测试收集项

    自动为异步测试添加 asyncio 标记。
    """
    for item in items:
        if "asyncio" in item.keywords:
            item.add_marker(pytest.mark.asyncio)
