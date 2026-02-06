# AGENTS.md

本文件为 AI 编程助手提供项目上下文和工作指南。

---

## Project Overview

**Novel Studio** 是一个 AI 驱动的小说创作工作室，基于 Python 3.12+ 和 LangChain 构建。

### 核心模块

| 模块 | 路径 | 功能 |
|------|------|------|
| **Bible** | `app/modules/bible/` | 世界观管理（背景、人物、规则的结构化存储） |
| **Outlines** | `app/modules/outlines/` | 大纲生成引擎（Substory、Chapter Blueprint、Scene 节拍） |
| **Materials** | `app/modules/materials/` | 素材供给层（Material Provider 抽象，上下文检索） |
| **Writing** | `app/modules/writing/` | 正文生成引擎（基于场景节拍的文本生成） |

### 技术栈

- **运行时**: Python 3.12+
- **包管理**: `uv` (Astral 生态)
- **LLM 框架**: LangChain + LangChain-OpenAI
- **数据存储**: SQLAlchemy + SQLite (异步: aiosqlite)
- **向量数据库**: ChromaDB
- **类型校验**: Pydantic v2

---

## Build and Test Commands

### 环境设置

```bash
# 安装依赖
uv sync

# 初始化数据库
uv run python init_db.py
```

### 运行项目

```bash
uv run python main.py
```

### 测试

```bash
# 运行所有测试
uv run python -m pytest test/

# 运行特定测试
uv run python -m pytest test/test_name.py -v
```

---

## Code Style Guidelines

### 工具链

```bash
# 代码检查并自动修复
uv run ruff check . --fix

# 代码格式化
uv run ruff format .

# 类型检查
uv run ty check
```

### 编码约定

1. **异步优先**: I/O 操作使用 `async/await`
2. **类型注解**: 所有函数必须有完整的类型注解
3. **Pydantic 校验**: 数据传输对象使用 Pydantic v2 模型
4. **命名规范**: 遵循 PEP 8，使用 `snake_case`
5. **行宽限制**: 100 字符 (`ruff` 配置)

### 提交前检查

```bash
uv run ruff check . --fix && uv run ruff format . && uv run ty check
```

---

## Testing Instructions

### 测试策略

- 单元测试放在 `test/` 目录
- 集成测试文件以 `test_*_flow.py` 命名
- 使用 `auto_test_*.py` 进行快速功能验证

### Mock LLM

测试时可使用 Mock 策略避免实际 API 调用，详见 `docs/ROADMAP.md` 中的测试体系规划。

---

## Security Considerations

### API 密钥管理

- 所有敏感配置存放在 `.env` 文件（已加入 `.gitignore`）
- 必需的环境变量：
  - `OPENAI_API_KEY`: OpenAI API 密钥
  - 其他 LLM 配置项见 `app/core/` 目录

### 数据安全

- 本地数据库文件存放在 `app/data/` 目录
- ChromaDB 向量数据库为本地存储
- 不要将用户生成内容提交到 Git

---

## Project Structure

```
novel_studio/
├── app/
│   ├── core/           # 核心配置（LLM、设置）
│   ├── db/             # 数据库连接与会话
│   ├── models/         # SQLAlchemy ORM 模型
│   ├── modules/        # 核心业务模块
│   │   ├── base/       # 基础抽象类
│   │   ├── materials/  # 素材供给层
│   │   ├── outlines/   # 大纲生成引擎
│   │   └── writing/    # 正文生成引擎
│   └── service/        # API 服务层
├── docs/               # 项目文档
│   ├── DEVELOPMENT.md  # 开发规范
│   └── ROADMAP.md      # 路线图
└── test/               # 测试文件
```

---

## Git Workflow

遵循 Feature Branch Workflow，详见 [docs/DEVELOPMENT.md](./docs/DEVELOPMENT.md)：

- `master`: 正式发布版本
- `develop`: 主开发分支
- `feat/*`: 功能开发分支

### 快速开始

```bash
# 同步并创建功能分支
git checkout develop && git pull origin develop && git checkout -b feat/task-name

# 提交代码
git add . && git commit -m "feat: 描述"

# 合并回 develop
git checkout develop && git pull origin develop && git merge feat/task-name
git push origin develop && git branch -d feat/task-name
```
