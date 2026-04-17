# Novel Studio 项目全面评估

> 评估时间：2026-04-14 | 分支：`feat/cli` | 提交：`09b3170`

---

## 0. 项目概览快照

| 指标 | 数值 |
|------|------|
| 源码文件 (`app/`) | 92 个 `.py` |
| 源码行数（不含 `__init__`） | ~3,782 行 |
| 测试文件 (`tests/`) | ~1,112 行 |
| 测试结果 | **97 passed, 6 failed, 5 errors** |
| Ruff lint | ✅ All checks passed |
| 未提交变更 | 无 |

---

## 1. 架构维度：评分 ⭐⭐⭐⭐ (4/5)

### 1.1 分层设计——高度吻合架构文档

项目实际代码已经忠实落地了 [ARCHITECTURE.md](file:///root/Project/cloud_workspace/novel_studio/docs/ARCHITECTURE.md) 中的五层架构：

```
Entry Layer        → main.py（占位）
Orchestrator Layer → app/orchestrator/  ✅ 已实现 chapter + outline
Service Layer      → app/service/       ✅ 已覆盖所有领域
Repository + UoW   → app/persistence/   ✅ 完整 UoW + Repository Groups
Engine Layer       → app/modules/       ✅ 最成熟的一层
```

> [!TIP]
> 这是目前项目最大的优势。五层分离干净，Engine 不碰持久化，Service 不跨领域，Orchestrator 只做编排。很多同类项目到这个阶段都还是"God Service"模式。

### 1.2 亮点

- **[ChapterOrchestrator](file:///root/Project/cloud_workspace/novel_studio/app/orchestrator/chapter.py)** 完整实现了 6 阶段流水线 + 状态推进 + 错误捕获，与架构文档 §9 的伪代码高度一致
- **[UnitOfWork](file:///root/Project/cloud_workspace/novel_studio/app/persistence/db/unit_of_work.py)** 使用 Repository Groups 分域，避免了"巨型 UoW"
- **MaterialProvider 协议** 实现了 Engine 层和 Service 层之间的依赖倒置
- **延迟导入 `__getattr__`** 模式统一应用于所有包级 `__init__.py`，冷启动性能好

### 1.3 问题

| 问题 | 位置 | 严重度 |
|------|------|--------|
| Entry Layer 完全空缺 | [main.py](file:///root/Project/cloud_workspace/novel_studio/main.py) 只有 `print("Hello")` | 🟡 中 |
| `materials.py` orchestrator 空文件 | [orchestrator/materials.py](file:///root/Project/cloud_workspace/novel_studio/app/orchestrator/materials.py) | 🟢 低 |
| Orchestrator 缺少 `__init__.py` 包导出 | `app/orchestrator/` | 🟢 低 |
| `resume()` / `submit_review()` 未实现 | [chapter.py:304-314](file:///root/Project/cloud_workspace/novel_studio/app/orchestrator/chapter.py#L304-L314) | 🟡 中 |

---

## 2. 代码健康度维度：评分 ⭐⭐⭐⭐ (4/5)

### 2.1 优点

- **Ruff lint 全部通过**，代码风格一致
- **类型注解覆盖完整**，所有函数签名都有类型标注
- **Pydantic v2 model** 统一用于 DTO / schema
- **命名规范**，PEP 8 + 中文注释清晰
- **异步一致**，所有 I/O 路径使用 `async/await`

### 2.2 代码层面具体问题

#### A. ChromaDB 操作使用同步 API（在异步方法中）

```python
# app/persistence/indexes/materials.py:67
self.vector_store.add_texts(...)        # 同步！在 async 方法内
# app/persistence/indexes/materials.py:77
results = self.vector_store.similarity_search(...)  # 同步！
```

> [!WARNING]
> `ChromaSnippetIndex` 的 `save_snippets` 和 `search_snippets` 方法签名是 `async`，但内部调用了 `Chroma` 的同步 API。这在高并发下会阻塞事件循环。应改用 `asyncio.to_thread()` 包装，或等待 langchain-chroma 提供真正的 async API。

#### B. 全局模块级副作用（Settings 实例化 + DB Engine 创建）

```python
# app/core/config.py:35
settings = Settings()          # 模块加载时立即实例化，要求 .env 存在

# app/persistence/db/engine.py:28-29
engine = create_db_engine()    # 模块加载时立即创建引擎
SessionFactory = create_session_factory(engine)
```

> [!IMPORTANT]
> 这导致 **任何 import 链触达这些模块都会触发 DB 连接创建和环境变量读取**。测试的 `conftest.py` 不得不在最顶部注入 `os.environ` 来绕过。建议改为惰性初始化（函数级 or `@lru_cache`）。

#### C. Orchestrator 直接硬编码内部实例化

```python
# app/orchestrator/chapter.py:63-69
class ChapterOrchestrator:
    def __init__(self) -> None:
        self.workflow_run_service = WorkflowRunService()         # 硬编码
        self.writing_service = WritingService(
            material_provider=HybridSearchMaterialProvider()     # 硬编码
        )
```

与之对比，所有 Service 类都接受 `uow_factory` / `engine_factory` 参数做依赖注入。**Orchestrator 是唯一没有 DI 的分层**，这让它很难被单元测试。

#### D. 错误类型过于模糊

```python
# 所有 service 的"找不到"都抛 ValueError
raise ValueError(f"Bible with id {bible_id} not found.")
raise ValueError(f"Workflow run {run_id} not found.")
raise ValueError(f"Written chapter with id ... not found.")
```

建议引入领域异常（如 `EntityNotFoundError`），方便上层按类型 catch 并返回合适的 HTTP 状态码。

#### E. `_run_to_completion` 的 except 过于宽泛

```python
# app/orchestrator/chapter.py:299-302
except Exception as e:
    await self.workflow_run_service.mark_failed(
        run_id, WorkflowErrorCode.LLM_CALL_ERROR, str(e)
    )
```

所有异常都被标记为 `LLM_CALL_ERROR`，但实际上可能是 `SQLITE_WRITE_ERROR` 或 `PARSE_ERROR`。丢失了 `WorkflowErrorCode` 中已经定义好的分类能力。

---

## 3. 测试维度：评分 ⭐⭐⭐ (3/5)

### 3.1 测试概况

| 类型 | 数量 | 状态 |
|------|------|------|
| 总测试 | 108 | — |
| 通过 | 97 | ✅ |
| 失败 | 6 | ❌ |
| 错误 | 5 | ❌ |

### 3.2 失败分析

**5 个快照失败**（stale inline-snapshot）：
- `test_chapter_scene_writing_context`
- `test_chapter_writing_context`
- `test_chapter_summary_context`
- `test_chapter_scene_writing_prompt_build_variables`
- `test_chapter_summary_prompt_build_variables`

原因：`ChapterBlueprint` schema 新增了 `substory_chapter_index` 字段，但快照没有同步更新。

> [!TIP]
> 修复方法：`uv run poe test-fix` 交互式更新快照即可。

**1 个 API 漂移失败**：
```
test_save_snippets_uses_uow_and_vector_store
TypeError: MaterialService.__init__() got an unexpected keyword argument 'vector_store'
```

原因：`MaterialService` 重构后将 `vector_store` 改为了 `snippet_index: SnippetIndex`，但测试未同步更新。

### 3.3 测试覆盖盲区

| 缺少覆盖的模块 | 风险 |
|----------------|------|
| `app/orchestrator/` | 🔴 **核心编排逻辑零测试** |
| `app/service/workflow.py` | 🔴 WorkflowRunService 无测试 |
| `app/service/outlines/chapter.py` | 🟡 ChapterService 无测试 |
| `app/service/post_writing.py` | 🟡 PostWritingService 无测试 |
| `app/service/writing.py` | 🟡 WritingService 仅空文件 |
| `app/persistence/db/unit_of_work.py` | 🟡 UoW 无直接测试 |
| `app/persistence/indexes/materials.py` | 🟡 ChromaSnippetIndex 无测试 |

> [!CAUTION]
> Orchestrator 和 Service 层是系统最核心的编排逻辑，但目前测试覆盖为零。这意味着 `_run_to_completion` 的 6 阶段流程、状态推进、错误处理路径全部没有自动化验证。

---

## 4. 工程成熟度维度：评分 ⭐⭐⭐⭐ (4/5)

### 4.1 做得好的

| 项目 | 评价 |
|------|------|
| 包管理 (`uv` + `pyproject.toml`) | ✅ 现代化，干净 |
| 任务自动化 (`poethepoet`) | ✅ 17 个 task，覆盖完整 |
| Lint 工具链 (`ruff` + `ty`) | ✅ 严格且全绿 |
| 测试框架搭建 | ✅ pytest-asyncio + FakeLLM + inline-snapshot |
| 文档体系 | ✅ 有 ARCHITECTURE / ROADMAP / TEST_PLAN / IDEAS |
| Git 分支策略 | ✅ 9 个功能分支，按领域拆分 |

### 4.2 欠缺的

| 项目 | 现状 | 建议 |
|------|------|------|
| CI/CD | ❌ 无 | 至少 GitHub Actions 跑 lint + test |
| 日志系统 | ❌ 无任何 logging 调用 | 引入 `structlog` 或标准 `logging` |
| 配置分环境 | ❌ 仅 `.env` | 区分 dev/test/prod 配置 |
| 数据库迁移 | ❌ 使用 `create_all` | 引入 Alembic |
| 错误监控 | ❌ 无 | 先 logging，后续可接 Sentry |

---

## 5. 设计一致性维度：评分 ⭐⭐⭐⭐⭐ (5/5)

项目最令人称赞的一点是：**代码实际实现与架构文档高度一致。**

| 架构文档章节 | 代码落地情况 |
|-------------|-------------|
| §3 五层分层 | ✅ 完全落地 |
| §4.1 LLM 不包在长事务里 | ✅ 每个 stage 独立 commit |
| §4.2 SQLite 是主事实源 | ✅ MaterialService 先写 SQL 再写 Chroma |
| §4.3 中间产物是一等公民 | ✅ blueprint/outline/summary 全部持久化 |
| §4.4 Orchestrator 管流程 Service 管领域 | ✅ 边界清晰 |
| §6 Workflow Run 设计 | ✅ 状态机完整实现 |
| §7.3 推荐 Service 列表 | ✅ 全部建立 |
| §8 Command DTO | ❌ 未采用，直接用散参数 |

> [!NOTE]
> 唯一未落地的是 §8 的 Command DTO 模式。当前各 Service 方法直接接收散参数，这在参数不多时可以接受，但随着 Orchestrator 变复杂，可能需要考虑引入。

---

## 6. 综合评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 架构设计 | ⭐⭐⭐⭐ | 五层分离清晰，个别占位未实现 |
| 代码健康度 | ⭐⭐⭐⭐ | lint 全绿，有几个需关注的设计隐患 |
| 测试质量 | ⭐⭐⭐ | Engine 层覆盖好，Service/Orchestrator 层空白 |
| 工程成熟度 | ⭐⭐⭐⭐ | 工具链完善，缺 CI/日志/迁移 |
| 设计一致性 | ⭐⭐⭐⭐⭐ | 代码忠实于架构文档，罕见 |
| **综合** | **⭐⭐⭐⭐ (4/5)** | **核心创作引擎成熟，编排层已搭好骨架，测试和工程基建需补强** |

---

## 7. 后续方向建议（分优先级）

### Phase 0: 立即修复（1-2 天）

- [ ] 运行 `uv run poe test-fix` 更新 5 个 stale snapshot
- [ ] 修复 `test_save_snippets_uses_uow_and_vector_store` 与 `MaterialService` 的 API 对齐
- [ ] 解决 5 个 test errors（可能也是同类问题）
- [ ] 让测试全绿作为后续开发的基线

### Phase 1: 补测试（3-5 天）

- [ ] 为 `ChapterOrchestrator` 编写集成测试（使用 FakeLLM + 内存 SQLite）
- [ ] 为 `WorkflowRunService` 编写单元测试（状态机转换覆盖）
- [ ] 为 `ChapterService` / `WritingService` / `PostWritingService` 补充 Service 层测试
- [ ] 为 `ChapterOrchestrator` 的 DI 支持重构 `__init__`

### Phase 2: 工程基建（1 周）

- [ ] 引入 `logging` / `structlog`，至少在 Orchestrator 和 Service 层打日志
- [ ] 引入 Alembic 做数据库迁移管理
- [ ] 添加 GitHub Actions CI：`ruff check` + `ruff format --check` + `pytest`
- [ ] 修复 ChromaDB 同步调用问题（`asyncio.to_thread` 包装）
- [ ] 引入领域异常（`EntityNotFoundError` / `WorkflowStateError`）替代 `ValueError`

### Phase 3: CLI 入口层（当前分支 `feat/cli`）

- [ ] 实现 `main.py` 作为 CLI 入口（建议使用 `click` 或 `typer`）
- [ ] 子命令设计：`bible brainstorm` / `bible create` / `substory create` / `chapter generate`
- [ ] 配置惰性初始化（解耦 import 时的副作用）

### Phase 4: 高级功能

- [ ] 实现 `ChapterOrchestrator.resume()`——从失败阶段恢复
- [ ] 实现 `ChapterOrchestrator.submit_review()`——人工审核流程
- [ ] `MaterialOrchestrator`——批量素材导入与管理
- [ ] Prompt 版本追踪——将 `model_name` / `prompt_version` 写入 artifacts

---

## 附录：关键文件路径快速导航

| 模块 | 文件 |
|------|------|
| 章节编排 | [orchestrator/chapter.py](file:///root/Project/cloud_workspace/novel_studio/app/orchestrator/chapter.py) |
| 大纲编排 | [orchestrator/outline.py](file:///root/Project/cloud_workspace/novel_studio/app/orchestrator/outline.py) |
| 工作流状态 | [domain/workflow.py](file:///root/Project/cloud_workspace/novel_studio/app/domain/workflow.py) |
| UoW 实现 | [persistence/db/unit_of_work.py](file:///root/Project/cloud_workspace/novel_studio/app/persistence/db/unit_of_work.py) |
| 仓库分组 | [persistence/repositories/groups.py](file:///root/Project/cloud_workspace/novel_studio/app/persistence/repositories/groups.py) |
| 写作引擎 | [modules/writing/engine.py](file:///root/Project/cloud_workspace/novel_studio/app/modules/writing/engine.py) |
| Hybrid Search | [service/material_providers.py](file:///root/Project/cloud_workspace/novel_studio/app/service/material_providers.py) |
| 架构文档 | [docs/ARCHITECTURE.md](file:///root/Project/cloud_workspace/novel_studio/docs/ARCHITECTURE.md) |
| 测试 FakeLLM | [tests/support/llm.py](file:///root/Project/cloud_workspace/novel_studio/tests/support/llm.py) |
