# Novel Studio

Novel Studio 是一个面向长篇网文创作流程的 AI 写作工作室，基于 Python 3.12、LangChain、SQLAlchemy 和 ChromaDB 构建。

当前项目已经具备核心创作引擎，但整体仍处于“引擎完成、系统集成中”的阶段：`outlines`、`materials`、`writing`、`post_writing` 已经有实现和测试覆盖，而应用入口、Service 编排层、API 和前端还没有形成完整产品闭环。

## 当前状态

- 已实现核心生成能力：Bible、Substory、Chapter Blueprint、Scene、Writing、Post-Writing。
- 已具备本地存储基础：SQLite + ChromaDB。
- 已建立较完整测试体系：截至 2026-03-25，`uv run poe test` 通过，`108 passed`，总覆盖率 `99.20%`。
- 主要缺口不在 Prompt 数量，而在编排层、对外接口、状态流转和文档同步。

## 核心模块

| 模块 | 路径 | 说明 |
|------|------|------|
| Base | `app/modules/base/` | 通用抽象、基础 schema、记忆对象 |
| Outlines | `app/modules/outlines/` | Bible、Substory、Chapter Blueprint、Scene 生成 |
| Materials | `app/modules/materials/` | 素材挖掘、结构化片段提取、向量存储接入 |
| Writing | `app/modules/writing/` | 基于场景节拍和素材的正文生成 |
| Post-Writing | `app/modules/post_writing/` | 章节总结、卷内累计总结 |
| DB | `app/db/`, `app/models/` | SQLite 会话、Chroma 向量库、ORM 模型 |
| Service | `app/service/` | 面向应用层的封装，当前仍在补齐阶段 |

## 开发重点

现阶段的优先级如下：

1. 收口完整创作闭环：把现有引擎串成稳定的端到端 workflow。
2. 做实 Service 和编排层：而不是继续堆积新的 Prompt 功能。
3. 明确 API 与流式输出边界：为前端 MVP 准备稳定接口。
4. 在系统边界稳定后，再做评估、Prompt 优化和高级后处理。

详细阶段规划见 [docs/ROADMAP.md](/root/Project/cloud_workspace/novel_studio/docs/ROADMAP.md)。

## 快速开始

### 环境准备

```bash
uv sync
uv run python init_db.py
```

### 运行

当前 `main.py` 仍是占位入口。现阶段更适合直接运行模块测试或后续接入的 API 服务。

```bash
uv run python main.py
```

### 测试

```bash
# 全量测试（并行 + 覆盖率）
uv run poe test

# 快速测试
uv run poe test-quick

# 只跑单元测试
uv run poe test-unit

# 只跑集成测试
uv run poe test-integration
```

在受限环境中如果 `uv` 默认缓存目录不可写，可临时指定：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run poe test
```

更详细的测试说明见 [docs/TEST_PLAN.md](/root/Project/cloud_workspace/novel_studio/docs/TEST_PLAN.md) 和 [tests/README.md](/root/Project/cloud_workspace/novel_studio/tests/README.md)。

## 代码质量

```bash
uv run ruff check . --fix
uv run ruff format .
uv run ty check
```

## 文档

- [docs/ROADMAP.md](/root/Project/cloud_workspace/novel_studio/docs/ROADMAP.md): 当前阶段判断与后续开发路线
- [docs/PROJECT_ASSESSMENT_AND_PLAN.md](/root/Project/cloud_workspace/novel_studio/docs/PROJECT_ASSESSMENT_AND_PLAN.md): 当前项目状态评估与后续开发规划
- [docs/DEVELOPMENT.md](/root/Project/cloud_workspace/novel_studio/docs/DEVELOPMENT.md): 开发规范
- [docs/TEST_PLAN.md](/root/Project/cloud_workspace/novel_studio/docs/TEST_PLAN.md): 测试策略与执行方式
- [docs/IDEAS.md](/root/Project/cloud_workspace/novel_studio/docs/IDEAS.md): 想法池与候选方向
