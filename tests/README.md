# 测试使用指南

本指南展示如何使用我们编写的现代化测试套件。

## 📁 文件结构

```
tests/
├── conftest.py                          # 全局 fixtures 和配置
├── test_demo.py                         # 原有示例测试
└── unit/
    └── test_materials_engine.py         # Materials Engine 测试套件 ⭐
```

## 🚀 快速开始

### 运行所有测试

```bash
# 运行所有测试（自动并行 + 覆盖率）
uv run pytest

# 只运行单元测试
uv run pytest -m unit

# 只运行 Materials 模块测试
uv run pytest tests/unit/test_materials_engine.py
```

### 运行特定测试类

```bash
# 只测试文本分割功能
uv run pytest tests/unit/test_materials_engine.py::TestTextSplitting -v

# 只测试 Schema 验证
uv run pytest tests/unit/test_materials_engine.py::TestMaterialSchemas -v

# 只测试素材挖掘
uv run pytest tests/unit/test_materials_engine.py::TestMaterialMining -v
```

### 运行特定测试函数

```bash
# 测试基础文本分割
uv run pytest tests/unit/test_materials_engine.py::TestTextSplitting::test_split_text_basic -v

# 测试 Schema 创建
uv run pytest tests/unit/test_materials_engine.py::TestMaterialSchemas::test_material_snippet_creation -v
```

## 🎯 测试特性展示

### 1. 使用类组织测试

```python
class TestTextSplitting:
    """相关测试组织在一起，提高可读性"""
    
    def test_split_text_basic(self):
        """测试基础功能"""
        pass
    
    def test_split_text_empty_string(self):
        """测试边界条件"""
        pass
```

**优势**：
- 逻辑清晰，易于导航
- 可以共享 setup/teardown
- 便于选择性运行

### 2. 参数化测试

```python
@pytest.mark.parametrize(
    ("text", "min_chunks"),
    [
        ("短文本", 1),
        ("中等长度的文本。" * 50, 1),
        ("很长的文本。" * 100, 2),
    ],
)
def test_split_text_parametrized(self, text: str, min_chunks: int):
    """一个测试，多组数据"""
    pass
```

**运行**：
```bash
uv run pytest tests/unit/test_materials_engine.py::TestTextSplitting::test_split_text_parametrized -v
```

**输出**：
```
test_split_text_parametrized[短文本-1] PASSED
test_split_text_parametrized[text1-1] PASSED
test_split_text_parametrized[text2-2] PASSED
```

### 3. Mock LLM 调用

```python
@pytest.mark.asyncio
async def test_mine_with_mock_llm(
    self,
    sample_mining_context: MaterialsMiningContext,
    mock_llm_chain: MagicMock,
):
    """使用 Mock 避免真实 API 调用"""
    with patch("app.modules.materials.engine.get_mining_chain", return_value=mock_llm_chain):
        engine = MaterialEngine()
        result = await engine.mine(sample_mining_context)
        
        # 验证 Mock 被调用
        mock_llm_chain.ainvoke.assert_called_once()
```

**优势**：
- 不产生 API 费用
- 测试速度快
- 可控的测试环境

### 4. dirty-equals 声明式断言

```python
from dirty_equals import IsListOrTuple, IsStr, IsNonNegative

def test_split_text_preserves_chinese_punctuation(self):
    """处理动态值的优雅方式"""
    chunks = engine.split_text(text)
    
    # 不关心具体值，只关心类型和约束
    assert chunks == IsListOrTuple(IsStr, length=IsNonNegative)
```

**运行**：
```bash
uv run pytest tests/unit/test_materials_engine.py::TestTextSplitting::test_split_text_preserves_chinese_punctuation -v
```

### 5. inline-snapshot 快照测试

```python
from inline_snapshot import snapshot

def test_material_snippet_prompt_generation(self, sample_material_snippet):
    """自动捕获预期输出"""
    prompt = sample_material_snippet.prompt(index=1)
    
    # 第一次运行时 snapshot() 为空
    assert prompt == snapshot()
```

**首次运行**（生成快照）：
```bash
uv run pytest tests/unit/test_materials_engine.py::TestMaterialSchemas::test_material_snippet_prompt_generation --inline-snapshot=fix
```

**后续运行**（验证快照）：
```bash
uv run pytest tests/unit/test_materials_engine.py::TestMaterialSchemas::test_material_snippet_prompt_generation
```

**更新快照**（当输出变化时）：
```bash
uv run pytest --inline-snapshot=fix
```

### 6. Fixtures 复用

```python
# conftest.py 中定义
@pytest.fixture
def sample_novel_text() -> str:
    """提供示例小说文本"""
    return "夜幕降临..."

# 测试中使用
def test_something(sample_novel_text: str):
    """自动注入 fixture"""
    assert len(sample_novel_text) > 0
```

**优势**：
- 减少重复代码
- 集中管理测试数据
- 自动清理资源

## 🏷️ 测试标记系统

### 按标记运行测试

```bash
# 只运行单元测试
uv run pytest -m unit

# 只运行集成测试
uv run pytest -m integration

# 跳过慢速测试
uv run pytest -m "not slow"

# 跳过 LLM 测试（避免费用）
uv run pytest -m "not llm"

# 组合条件
uv run pytest -m "unit and not slow"
```

### 标记说明

| 标记 | 说明 | 示例 |
|------|------|------|
| `@pytest.mark.unit` | 单元测试 | 测试单个函数 |
| `@pytest.mark.integration` | 集成测试 | 测试多个组件协作 |
| `@pytest.mark.slow` | 慢速测试 | 耗时 > 1s |
| `@pytest.mark.llm` | 真实 LLM 调用 | 产生 API 费用 |
| `@pytest.mark.asyncio` | 异步测试 | 自动添加 |

## 📊 覆盖率报告

### 生成覆盖率报告

```bash
# 运行测试并生成覆盖率
uv run pytest

# 查看终端报告（自动显示）
# --cov-report=term-missing 已配置

# 查看 HTML 详细报告
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### 查看特定模块覆盖率

```bash
# 只看 Materials 模块
uv run pytest --cov=app.modules.materials --cov-report=term-missing

# 只看 Writing 模块
uv run pytest --cov=app.modules.writing --cov-report=term-missing
```

## 🐛 调试技巧

### 显示打印输出

```bash
# 显示 print() 输出
uv run pytest -s

# 详细输出 + 打印
uv run pytest -v -s
```

### 调试单个测试

```bash
# 运行单个测试，显示完整 traceback
uv run pytest tests/unit/test_materials_engine.py::TestTextSplitting::test_split_text_basic -vv

# 在第一个失败处停止
uv run pytest -x

# 使用 pdb 调试
uv run pytest --pdb
```

### 查看失败详情

```bash
# 只运行上次失败的测试
uv run pytest --lf

# 先运行失败的，再运行其他
uv run pytest --ff
```

## 🎨 最佳实践示例

### AAA 模式（Arrange-Act-Assert）

```python
def test_split_text_basic(self):
    # Arrange - 准备测试数据
    engine = MaterialEngine()
    text = "第一段。\n\n第二段。"
    
    # Act - 执行操作
    chunks = engine.split_text(text)
    
    # Assert - 验证结果
    assert len(chunks) > 0
```

### 清晰的测试命名

```python
# ✅ 好的命名
def test_split_text_empty_string(self):
    """测试空字符串分割"""
    pass

# ❌ 不好的命名
def test_1(self):
    pass
```

### 完整的文档字符串

```python
def test_mine_with_mock_llm(self):
    """测试素材挖掘（Mock LLM）
    
    使用 patch 替换真实的 LLM chain。
    验证：
    1. 返回正确的数据结构
    2. Mock 被正确调用
    """
    pass
```

### 边界条件测试

```python
class TestEdgeCases:
    """专门测试边界条件"""
    
    def test_split_text_empty_string(self):
        """空字符串"""
        pass
    
    def test_split_very_long_text(self):
        """超长文本"""
        pass
    
    def test_split_text_with_special_characters(self):
        """特殊字符"""
        pass
```

## 📈 测试进度追踪

### 当前覆盖率

运行以下命令查看当前覆盖率：

```bash
uv run pytest --cov=app --cov-report=term-missing
```

### 目标

- Materials 模块：80%+ ✅
- 整体项目：70%+ 🎯

## 🔄 CI/CD 集成

### GitHub Actions 示例

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          uv sync
          uv run pytest -m "not slow and not llm"
```

## 📚 参考资源

- [pytest 官方文档](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [dirty-equals](https://dirty-equals.helpmanual.io/)
- [inline-snapshot](https://15r10nk.github.io/inline-snapshot/)

## 🎓 下一步

1. **运行示例测试**：
   ```bash
   uv run pytest tests/unit/test_materials_engine.py -v
   ```

2. **查看覆盖率报告**：
   ```bash
   uv run pytest
   open htmlcov/index.html
   ```

3. **编写更多测试**：
   - 参考 `test_materials_engine.py` 的模式
   - 为其他模块编写类似的测试

4. **集成到开发流程**：
   - 提交前运行测试
   - 设置 pre-commit hook
   - 配置 CI/CD

---

**Happy Testing! 🎉**
