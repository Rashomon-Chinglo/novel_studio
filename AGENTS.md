# AGENTS.md

本文件为 AI 编程助手提供项目上下文和工作指南。

---

## Project Overview

**Novel Studio** 是一个 AI 驱动的小说创作工作室，基于 Python 3.12+ 和 LangChain 构建。

项目当前状态不是“从零开始”，而是：

**核心创作引擎已具备，正在补齐系统编排层、Service 层、入口层和文档。**

### 核心模块

| 模块 | 路径 | 功能 |
|------|------|------|
| **Base** | `app/modules/base/` | 通用抽象、基础 schema、记忆对象 |
| **Outlines** | `app/modules/outlines/` | Bible、Substory、Chapter Blueprint、Scene 节拍生成 |
| **Materials** | `app/modules/materials/` | 素材挖掘、结构化提取、向量存储接入 |
| **Writing** | `app/modules/writing/` | 基于场景节拍和素材的正文生成 |
| **Post-Writing** | `app/modules/post_writing/` | 章节总结、卷内累计总结 |
| **Service** | `app/service/` | 应用层封装，当前仍在补齐 |

### 技术栈

- **运行时**: Python 3.12+
- **包管理**: `uv`
- **LLM 框架**: LangChain + LangChain-OpenAI
- **数据存储**: SQLAlchemy + SQLite
- **向量数据库**: ChromaDB
- **类型校验**: Pydantic v2

---

## Build and Test Commands

### 环境设置

```bash
uv sync
uv run python scripts/init_persistence.py
```

### 运行项目

```bash
uv run python main.py
```

注：`main.py` 当前仍是占位入口，实际开发阶段更应关注模块测试和后续 API 入口。

### 测试

```bash
# 全量测试
uv run poe test

# 快速测试
uv run poe test-quick

# 单元测试
uv run poe test-unit

# 集成测试
uv run poe test-integration
```

如果环境对默认缓存目录有限制：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run poe test
```

---

## Code Style Guidelines

### 工具链

```bash
uv run ruff check . --fix
uv run ruff format .
uv run ty check
```

### 编码约定

1. **异步优先**: I/O 操作使用 `async/await`
2. **类型注解**: 所有函数必须有完整类型注解
3. **Pydantic 校验**: DTO 优先使用 Pydantic v2
4. **命名规范**: 遵循 PEP 8，使用 `snake_case`
5. **行宽限制**: 100 字符

### 提交前检查

```bash
uv run ruff check . --fix
uv run ruff format .
uv run ty check
uv run poe test-quick
```

---

## Testing Instructions

### 测试策略

- 单元测试位于 `tests/unit/`
- 集成测试位于 `tests/integration/`
- 默认使用 Fake LLM 避免真实 API 调用
- Service 层和未来的 orchestrator 是下一轮重点补强区域

### Mock LLM

测试支持通过 `tests/support/llm.py` 注入 Fake LLM。优先使用 Mock/Fake 验证 workflow、prompt 和 context，而不是依赖真实模型输出。

---

## Security Considerations

### API 密钥管理

- 所有敏感配置存放在 `.env`
- 必需环境变量：
  - `OPENAI_API_KEY`
  - `JINA_API_KEY`

### 数据安全

- SQLite 和 ChromaDB 数据默认保存在 `app/data/`
- 不要将用户生成内容或本地数据库提交到 Git

---

## Project Structure

```text
novel_studio/
├── app/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── modules/
│   │   ├── base/
│   │   ├── materials/
│   │   ├── outlines/
│   │   ├── post_writing/
│   │   └── writing/
│   └── service/
├── docs/
├── tests/
└── main.py
```

---

## Git Workflow

遵循 Feature Branch Workflow，详见 `docs/DEVELOPMENT.md`。

- `master`: 稳定发布分支
- `develop`: 主开发分支
- `feat/*`: 功能开发分支
