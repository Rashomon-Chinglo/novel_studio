# Novel Studio 架构设计

本文档描述 Novel Studio 在当前阶段的应用层架构，重点解决下面几个问题：

- 如何把现有 `modules/*` 能力收口成稳定的创作 workflow
- 如何补齐 `service` 与 `orchestrator`，但不破坏已有 engine 层
- 如何让“可保存、可复查、可恢复、可测试”成为真实能力，而不是文档口号

更新日期：2026-03-29

---

## 1. 当前判断

项目目前不是“缺 AI 功能”，而是“缺稳定编排和状态管理”。

现状可以概括为：

- `app/modules/*` 已经具备较完整的生成能力
- `app/service/materials.py` 证明了 service 层方向是对的，但实现仍偏早期
- `app/service/outlines/*.py`、`app/service/writing.py` 还基本空缺
- 还没有统一的 workflow run、阶段状态、恢复机制
- 现有数据库模型只覆盖了部分最终产物，没有覆盖中间阶段产物与运行状态

所以阶段 1 的核心，不是继续扩 prompt，而是建立一套足够稳的“应用骨架”。

---

## 2. 架构目标

### 2.1 这一阶段要达成的能力

- 从单一入口触发单章创作
- 每个阶段都可以单独保存与回看
- 章节创作失败后，可以定位到失败阶段
- 章节创作可以从最近一个已完成阶段继续执行，而不是整章重跑
- 后续接 API / 前端时，不需要直接暴露 `modules/*` 细节

### 2.2 这一阶段不要追求的能力

- 不在阶段 1 引入复杂插件化
- 不在阶段 1 引入多租户与权限
- 不把 orchestrator 做成通用工作流引擎
- 不为了“纯粹架构美感”引入过多抽象层

目标是：先把单章闭环做稳，再扩。

---

## 3. 推荐分层

建议采用下面这套分层，而不是只停留在“Engine / Service / Orchestrator”三个概念词。

```text
┌────────────────────────────────────────────────────────────┐
│ Entry Layer                                                │
│ main.py / future API / CLI                                 │
├────────────────────────────────────────────────────────────┤
│ Orchestrator Layer                                         │
│ chapter workflow / substory workflow                       │
├────────────────────────────────────────────────────────────┤
│ Application Service Layer                                  │
│ outlines / writing / post-writing / materials              │
├────────────────────────────────────────────────────────────┤
│ Repository + UnitOfWork Layer                              │
│ SQLAlchemy models / session / persistence adapters         │
├────────────────────────────────────────────────────────────┤
│ Engine Layer                                               │
│ prompt + chain + context + schema                          │
└────────────────────────────────────────────────────────────┘
```

### 3.1 Entry Layer

职责：

- 接收外部调用
- 参数校验
- 调用 orchestrator
- 返回结构化结果

不负责：

- 业务编排
- 数据库读写细节
- LLM 调用细节

### 3.2 Orchestrator Layer

职责：

- 串联多个 service，定义完整流程顺序
- 驱动 workflow run 状态推进
- 控制从哪一步恢复执行
- 处理跨 service 的错误边界

不负责：

- 直接写 prompt
- 直接操作 ORM
- 直接依赖具体 LLM chain

### 3.3 Application Service Layer

职责：

- 面向单一领域提供应用接口
- 组织输入 DTO 到 engine context 的映射
- 读写本领域对象
- 抛出明确的领域异常

不负责：

- 跨阶段总编排
- 长事务管理
- 跨多个领域对象的一致性协调

### 3.4 Repository + UnitOfWork Layer

职责：

- 封装 SQLAlchemy session、模型、查询、保存
- 提供短事务边界
- 支撑 orchestrator / service 的幂等与恢复

不负责：

- 调用 LLM
- 决定业务流程

### 3.5 Engine Layer

职责：

- prompt 构造
- LLM 调用
- 输出结构化 schema

不负责：

- 持久化
- run 状态推进
- 业务重试策略

---

## 4. 核心原则

### 4.1 LLM 调用绝不能包在长事务里

章节创作链路很长，不能这样做：

- 打开一个数据库事务
- 连续调 4 到 6 个 LLM 阶段
- 最后一次性提交

这会导致：

- 事务持有时间过长
- SQLite 锁竞争风险增大
- 任意中途失败都会让前面成功阶段完全丢失
- 无法做阶段级恢复

因此本项目应采用：

- LLM 计算在事务外执行
- 每个阶段成功后，立即短事务落库
- workflow run 状态同步推进

### 4.2 SQLite 是主事实源，Chroma 是派生索引

现有 `MaterialService` 已经体现出 SQL 与向量库是两条写链路。[app/service/materials.py](/root/Project/cloud_workspace/novel_studio/app/service/materials.py)

设计上必须明确：

- SQLite 是主存储，业务是否成功以 SQLite 为准
- Chroma 是检索加速层，不应决定主 workflow 是否成功
- 向量写入失败时，允许降级并记录待补写状态

也就是说：

- “写 SQL 成功，写 Chroma 失败” 应视为部分降级，不应把章节主流程整体回滚
- 需要补一套 backfill / retry 机制，而不是试图跨 SQLite 和 Chroma 做伪分布式事务

### 4.3 中间产物是一等公民

如果只保存最终正文，系统就无法做到：

- 复盘 blueprint 是否合理
- 复用已生成 scene outline
- 失败后从中间阶段继续
- 对每阶段产出做测试与评估

因此以下对象都应允许持久化：

- Bible
- Substory
- Chapter Blueprint
- Chapter Outline（场景与 beats）
- Written Chapter
- Chapter Summary
- Cumulative Substory Summary
- Workflow Run / Stage State

### 4.4 Orchestrator 管流程，Service 管领域

不要让 `ChapterService` 一边处理 chapter，一边去加载 bible、substory、summary 全部上下文。

更稳的边界是：

- `BibleService` 负责 bible
- `SubstoryService` 负责 substory
- `ChapterService` 负责 blueprint / chapter outline
- `WritingService` 负责正文生成
- `PostWritingService` 负责 summary 生成与保存
- `WorkflowRunService` 负责运行状态记录

Orchestrator 负责把这些拼起来。

---

## 5. 领域对象与持久化建议

### 5.1 已存在的持久化对象

当前已有：

- `bibles`
- `substories`
- `chapters`
- `snippets`

参考：

- [app/models/outline.py](/root/Project/cloud_workspace/novel_studio/app/models/outline.py)
- [app/models/snippet.py](/root/Project/cloud_workspace/novel_studio/app/models/snippet.py)

这些表还不够支撑完整 workflow。

### 5.2 建议新增的持久化对象

建议至少补下面几类表或等价聚合对象。

#### A. 运行状态

`workflow_runs`

建议字段：

- `id`
- `workflow_type`
- `status`
- `current_stage`
- `bible_id`
- `substory_id`
- `chapter_index`
- `error_code`
- `error_message`
- `retry_count`
- `started_at`
- `finished_at`

用途：

- 记录某次“创建第 N 章”的执行过程
- 支撑重试、恢复、监控、排错

#### B. 阶段产物快照

可以选择“每种产物独立表”，也可以先用“统一 artifact 表”。

更推荐先独立建表，便于查询和后续约束：

- `chapter_blueprints`
- `chapter_outlines`
- `written_chapters`
- `chapter_summaries`
- `substory_cumulative_summaries`

每类表至少应有：

- `id`
- 上游关联 id
- `workflow_run_id`
- `content`
- `status`
- `created_at`

#### C. 恢复与审计信息

建议给关键产物增加下面这些字段中的一部分：

- `source_stage`
- `model_name`
- `prompt_version`
- `raw_output`
- `parse_error`

阶段 1 不一定全部实现，但文档里应该先把这个方向定下来。

### 5.3 如果不想现在就建很多表

可以先采用折中方案：

- 新建 `workflow_runs`
- 新建 `chapter_generation_artifacts`

其中 `chapter_generation_artifacts` 可包含：

- `id`
- `workflow_run_id`
- `artifact_type`
- `content`
- `status`
- `created_at`

`artifact_type` 取值例如：

- `chapter_blueprint`
- `chapter_outline`
- `written_chapter`
- `chapter_summary`
- `cumulative_summary`

这比完全不存中间结果要好很多，也足够支撑阶段 1。

---

## 6. Workflow Run 设计

`ChapterOrchestrator` 不应只返回一个 `chapter_id`，还应该围绕 `workflow_run_id` 运转。

### 6.1 推荐状态机

`workflow_runs.status`

- `pending`
- `running`
- `succeeded`
- `failed`
- `partially_succeeded`

`workflow_runs.current_stage`

- `load_context`
- `generate_blueprint`
- `generate_outline`
- `write_chapter`
- `summarize_chapter`
- `update_cumulative_summary`
- `persist_final_refs`

### 6.2 推荐执行模型

单章流程建议这样跑：

1. 创建 `workflow_run`
2. 加载 bible / substory / summary 等输入
3. 生成 blueprint
4. 立即保存 blueprint artifact，并更新 run stage
5. 生成 chapter outline
6. 立即保存 outline artifact，并更新 run stage
7. 生成正文
8. 立即保存 written chapter artifact，并更新 run stage
9. 生成 chapter summary
10. 保存 chapter summary artifact，并更新 run stage
11. 生成 cumulative summary
12. 保存 cumulative summary artifact，并更新 run stage
13. 提交最终“引用关系”或“主记录指针”
14. 将 run 标记为 `succeeded`

这个模型的优点：

- 任意阶段失败，都能知道停在哪
- 下一次可以从最近成功阶段恢复
- 测试时可以只验证某阶段 artifact 是否正确保存

### 6.3 恢复策略

`resume` 不应该只是“重新执行一遍 create_chapter”，而应该支持：

- 从 `failed` 的 run 继续
- 若某 artifact 已存在且状态为成功，则跳过对应阶段
- 允许强制从指定阶段重跑

建议后续预留接口：

```python
class ChapterOrchestrator:
    async def create_chapter(...) -> ChapterWorkflowResult: ...
    async def resume_run(self, workflow_run_id: str) -> ChapterWorkflowResult: ...
    async def rerun_from_stage(
        self,
        workflow_run_id: str,
        stage: ChapterStage,
    ) -> ChapterWorkflowResult: ...
```

---

## 7. Service 层设计

### 7.1 Service 的基本约束

建议每个 service 至少提供这三类能力：

- `generate_*`：调用 engine，返回 schema
- `save_*`：保存该领域对象
- `get_*` / `list_*`：读取该领域对象

必要时可额外提供：

- `mark_*`：更新状态
- `find_latest_*`：查最近有效对象
- `load_by_run_*`：按 workflow run 查询产物

### 7.2 Service 不要直接暴露 ORM

service 的输入输出应是 Pydantic DTO 或 domain schema，而不是 SQLAlchemy model。

这样做的好处：

- API 层不会依赖 ORM
- orchestrator 可以保持更清晰
- 测试更容易用 fake / mock 替换

### 7.3 推荐的 Service 列表

```text
app/service/
├── materials.py
├── writing.py
├── post_writing.py
├── workflow_run.py
└── outlines/
    ├── bible.py
    ├── substory.py
    └── chapter.py
```

### 7.4 BibleService

职责：

- 生成 bible
- 保存 bible
- 读取 bible

建议接口：

```python
class BibleService:
    async def generate(self, premise: str) -> Bible: ...
    async def save(self, bible: Bible) -> str: ...
    async def get(self, bible_id: str) -> Bible: ...
```

### 7.5 SubstoryService

职责：

- 基于 bible 生成 substory
- 保存 substory
- 查询某个 bible 下的 substories

建议接口：

```python
class SubstoryService:
    async def generate(self, bible: Bible, user_input: str | None = None) -> Substory: ...
    async def save(self, bible_id: str, substory: Substory, order_index: int) -> str: ...
    async def get(self, substory_id: str) -> Substory: ...
    async def list_by_bible(self, bible_id: str) -> list[Substory]: ...
```

### 7.6 ChapterService

职责只限于 chapter domain：

- 生成 blueprint
- 生成 chapter outline
- 保存 blueprint / outline
- 读取 blueprint / outline

不建议在这里放：

- `load_bible`
- `load_substory`
- `load_summaries`

建议接口：

```python
class ChapterService:
    async def generate_blueprint(self, command: GenerateChapterBlueprintCommand) -> ChapterBlueprint: ...
    async def generate_outline(self, command: GenerateChapterOutlineCommand) -> ChapterOutline: ...

    async def save_blueprint(
        self,
        workflow_run_id: str,
        substory_id: str,
        blueprint: ChapterBlueprint,
    ) -> str: ...

    async def save_outline(
        self,
        workflow_run_id: str,
        substory_id: str,
        outline: ChapterOutline,
    ) -> str: ...

    async def get_latest_blueprint(self, substory_id: str, chapter_index: int) -> ChapterBlueprint | None: ...
    async def get_latest_outline(self, substory_id: str, chapter_index: int) -> ChapterOutline | None: ...
```

这里的 `ChapterOutline` 对应当前 `app.modules.outlines.schemas.chapter.Chapter`。[app/modules/outlines/schemas/chapter.py](/root/Project/cloud_workspace/novel_studio/app/modules/outlines/schemas/chapter.py)

### 7.7 WritingService

`WritingEngine` 当前已经通过 `MaterialProvider` 协议做了依赖倒置。[app/modules/writing/providers.py](/root/Project/cloud_workspace/novel_studio/app/modules/writing/providers.py)

因此 `WritingService` 的设计应顺着这个方向走，不要直接把 `MaterialService` 强耦合进 engine。

职责：

- 组织 writing 所需完整上下文
- 调用 `WritingEngine`
- 保存 written chapter

建议接口：

```python
class WritingService:
    async def write(self, command: WriteChapterCommand) -> WrittenChapter: ...
    async def save(
        self,
        workflow_run_id: str,
        substory_id: str,
        written: WrittenChapter,
        order_index: int,
        title: str,
    ) -> str: ...
    async def get(self, written_chapter_id: str) -> WrittenChapter: ...
```

这里的 `WrittenChapter` 对应当前 `app.modules.writing.schemas.Chapter`。[app/modules/writing/schemas.py](/root/Project/cloud_workspace/novel_studio/app/modules/writing/schemas.py)

### 7.8 PostWritingService

职责：

- 生成 chapter summary
- 生成 cumulative summary
- 保存两类 summary
- 查询最近 summary

建议接口：

```python
class PostWritingService:
    async def summarize_chapter(self, command: SummarizeChapterCommand) -> ChapterSummary: ...
    async def update_cumulative(
        self,
        command: UpdateCumulativeSummaryCommand,
    ) -> CumulativeSubstorySummary: ...

    async def save_chapter_summary(
        self,
        workflow_run_id: str,
        chapter_id: str | None,
        substory_id: str,
        summary: ChapterSummary,
    ) -> str: ...

    async def save_cumulative_summary(
        self,
        workflow_run_id: str,
        substory_id: str,
        summary: CumulativeSubstorySummary,
    ) -> str: ...

    async def get_latest_chapter_summary(self, substory_id: str) -> ChapterSummary | None: ...
    async def get_latest_cumulative_summary(
        self,
        substory_id: str,
    ) -> CumulativeSubstorySummary | None: ...
```

### 7.9 WorkflowRunService

这是原文档里缺失但实际很关键的一层。

建议接口：

```python
class WorkflowRunService:
    async def create_chapter_run(
        self,
        bible_id: str,
        substory_id: str,
        chapter_index: int,
    ) -> WorkflowRun: ...

    async def mark_stage(self, run_id: str, stage: ChapterStage) -> None: ...
    async def mark_failed(self, run_id: str, stage: ChapterStage, error: Exception) -> None: ...
    async def mark_succeeded(self, run_id: str) -> None: ...
    async def get(self, run_id: str) -> WorkflowRun: ...
```

---

## 8. Command DTO 设计

相比把一堆散参数直接塞进 service 方法，更推荐明确的 command DTO。

原因：

- 接口更稳定
- 参数不会随着流程增加而不断膨胀
- 更适合测试
- 更适合未来 API 请求体直接映射

建议增加一组 `app/service/dto/`：

```text
app/service/dto/
├── outlines.py
├── writing.py
├── post_writing.py
└── workflow.py
```

示例：

```python
class GenerateChapterBlueprintCommand(BaseModel):
    bible: Bible
    substory: Substory
    logic_nodes_to_process: ChapterOriginalSubstoryNodes
    pre_chapter_summary: ChapterSummary
    cumulative_substory_summary: CumulativeSubstorySummary


class WriteChapterCommand(BaseModel):
    bible: Bible
    substory: Substory
    original_logic_nodes: ChapterOriginalSubstoryNodes
    chapter_blueprint: ChapterBlueprint
    chapter_outline: ChapterOutline
    pre_chapter_summary: ChapterSummary
    cumulative_substory_summary: CumulativeSubstorySummary
    previous_content: str
```

这和当前 engine context 也更一致：

- [app/modules/outlines/context/chapter.py](/root/Project/cloud_workspace/novel_studio/app/modules/outlines/context/chapter.py)
- [app/modules/writing/context.py](/root/Project/cloud_workspace/novel_studio/app/modules/writing/context.py)
- [app/modules/post_writing/context.py](/root/Project/cloud_workspace/novel_studio/app/modules/post_writing/context.py)

---

## 9. Orchestrator 设计

### 9.1 ChapterOrchestrator 职责

它只负责：

- 创建并维护 workflow run
- 调用多个 service
- 推进阶段状态
- 控制失败后的停止与恢复

它不负责：

- 拼 prompt
- 直接操作 session
- 直接解析 LLM 原始输出

### 9.2 推荐流程

```text
create workflow run
    ↓
load bible / substory / existing summaries
    ↓
generate blueprint
    ↓
save blueprint artifact + mark stage
    ↓
generate chapter outline
    ↓
save outline artifact + mark stage
    ↓
write chapter
    ↓
save written chapter + mark stage
    ↓
summarize chapter
    ↓
save chapter summary + mark stage
    ↓
update cumulative summary
    ↓
save cumulative summary + mark stage
    ↓
mark run succeeded
```

### 9.3 推荐伪代码

```python
class ChapterOrchestrator:
    def __init__(
        self,
        workflow_run_service: WorkflowRunService,
        bible_service: BibleService,
        substory_service: SubstoryService,
        chapter_service: ChapterService,
        writing_service: WritingService,
        post_writing_service: PostWritingService,
    ):
        ...

    async def create_chapter(
        self,
        bible_id: str,
        substory_id: str,
        chapter_index: int,
    ) -> ChapterWorkflowResult:
        run = await self.workflow_run_service.create_chapter_run(
            bible_id=bible_id,
            substory_id=substory_id,
            chapter_index=chapter_index,
        )

        try:
            await self.workflow_run_service.mark_stage(run.id, ChapterStage.LOAD_CONTEXT)
            bible = await self.bible_service.get(bible_id)
            substory = await self.substory_service.get(substory_id)
            pre_summary = await self.post_writing_service.get_latest_chapter_summary(substory_id)
            cumulative = await self.post_writing_service.get_latest_cumulative_summary(substory_id)

            await self.workflow_run_service.mark_stage(run.id, ChapterStage.GENERATE_BLUEPRINT)
            blueprint = await self.chapter_service.generate_blueprint(...)
            blueprint_id = await self.chapter_service.save_blueprint(run.id, substory_id, blueprint)

            await self.workflow_run_service.mark_stage(run.id, ChapterStage.GENERATE_OUTLINE)
            outline = await self.chapter_service.generate_outline(...)
            outline_id = await self.chapter_service.save_outline(run.id, substory_id, outline)

            await self.workflow_run_service.mark_stage(run.id, ChapterStage.WRITE_CHAPTER)
            written = await self.writing_service.write(...)
            written_id = await self.writing_service.save(...)

            await self.workflow_run_service.mark_stage(run.id, ChapterStage.SUMMARIZE_CHAPTER)
            chapter_summary = await self.post_writing_service.summarize_chapter(...)
            chapter_summary_id = await self.post_writing_service.save_chapter_summary(
                run.id, written_id, substory_id, chapter_summary
            )

            await self.workflow_run_service.mark_stage(
                run.id, ChapterStage.UPDATE_CUMULATIVE_SUMMARY
            )
            cumulative_summary = await self.post_writing_service.update_cumulative(...)
            cumulative_summary_id = await self.post_writing_service.save_cumulative_summary(
                run.id, substory_id, cumulative_summary
            )

            await self.workflow_run_service.mark_succeeded(run.id)
            return ChapterWorkflowResult(
                workflow_run_id=run.id,
                blueprint_id=blueprint_id,
                outline_id=outline_id,
                written_chapter_id=written_id,
                chapter_summary_id=chapter_summary_id,
                cumulative_summary_id=cumulative_summary_id,
            )
        except Exception as exc:
            await self.workflow_run_service.mark_failed(run.id, run.current_stage, exc)
            raise
```

### 9.4 恢复优先于“统一提交”

原始版本里“最后统一持久化”的思路不适合当前项目。

更适合当前仓库的策略是：

- 每阶段保存
- run 驱动恢复
- 最终结果只是对阶段产物的聚合视图

这样既符合 SQLite 特性，也更接近 LLM workflow 的真实工程需求。

---

## 10. 错误边界

### 10.1 错误分类

建议至少区分：

- `LLMCallError`
- `SchemaParseError`
- `PersistenceError`
- `VectorIndexError`
- `WorkflowStateError`
- `NotFoundError`

### 10.2 推荐处理策略

| 类型 | 场景 | 策略 |
|------|------|------|
| `LLMCallError` | timeout / rate limit / transient upstream failure | 有限重试，记录 run 错误 |
| `SchemaParseError` | 输出不符合 schema | 保存 raw output，终止当前阶段 |
| `PersistenceError` | SQLite 写失败 | 当前阶段失败，run 标记 failed |
| `VectorIndexError` | Chroma 写失败 | 主流程可降级成功，记录待补写 |
| `WorkflowStateError` | run 状态非法 | 拒绝继续执行 |
| `NotFoundError` | bible / substory / artifact 不存在 | 快速失败 |

### 10.3 重试边界

不要在 orchestrator 顶层做“整章无脑重试”。

更合理的是：

- engine 调用失败时，对当前阶段有限重试
- parse 失败通常不自动重试
- persistence 失败不自动重试写库多次，避免重复数据
- rerun / resume 由 workflow run 驱动

---

## 11. 测试策略与架构配合

当前测试已经对 `WritingEngine` 的 `MaterialProvider` 协议做了良好隔离。[tests/conftest.py](/root/Project/cloud_workspace/novel_studio/tests/conftest.py)

后续应按分层补测试：

### 11.1 Engine 测试

目标：

- 保证 prompt/context/schema 接线正确
- 继续使用 Fake LLM

### 11.2 Service 测试

目标：

- 保证 DTO 到 context 的映射正确
- 保证持久化格式正确
- 保证读写与查询逻辑正确

### 11.3 Orchestrator 测试

目标：

- 保证阶段顺序正确
- 保证 run 状态推进正确
- 保证失败时停在正确阶段
- 保证 resume / rerun 行为正确

建议新增：

- `tests/unit/service/`
- `tests/unit/orchestrator/`
- `tests/integration/workflows/`

---

## 12. 目录建议

阶段 1 落地后，建议目录演进到下面这样：

```text
app/
├── core/
├── db/
├── models/
├── modules/
│   ├── base/
│   ├── materials/
│   ├── outlines/
│   ├── post_writing/
│   └── writing/
├── orchestrator/
│   ├── __init__.py
│   ├── chapter.py
│   └── substory.py
├── service/
│   ├── dto/
│   │   ├── outlines.py
│   │   ├── post_writing.py
│   │   ├── workflow.py
│   │   └── writing.py
│   ├── workflow_run.py
│   ├── materials.py
│   ├── writing.py
│   ├── post_writing.py
│   └── outlines/
│       ├── bible.py
│       ├── substory.py
│       └── chapter.py
└── repository/
    ├── outline.py
    ├── summary.py
    ├── workflow_run.py
    └── writing.py
```

如果当前不想新建 `repository/` 目录，也可以先把 repository 逻辑写在 service 内部，但文档上要明确这是阶段性妥协，而不是最终职责边界。

---

## 13. 落地顺序

按依赖和风险排序，建议这样推进：

### Step 1

补 `workflow_runs` 模型与 `WorkflowRunService`

原因：

- 没有 run，后面所有恢复、阶段保存、排错都无从谈起

### Step 2

补 `PostWritingService` 的持久化模型

原因：

- summary 是 chapter workflow 的关键输入
- 当前完全没有 summary 持久化承载物

### Step 3

补 `ChapterService`

包括：

- `generate_blueprint`
- `generate_outline`
- `save_blueprint`
- `save_outline`

### Step 4

补 `WritingService`

包括：

- `write`
- `save`
- `get`

### Step 5

实现 `ChapterOrchestrator`

先只做：

- `create_chapter`
- `resume_run`

### Step 6

为单章 workflow 补齐单元测试和集成测试

### Step 7

再考虑 `SubstoryOrchestrator`

---

## 14. 一句话结论

这个项目下一步最合理的架构，不是“再加一层 service 就完了”，而是：

**以 workflow run 为中心，用 orchestrator 驱动阶段执行，用 service 管领域对象，用短事务保存阶段产物，用 SQLite 作为主事实源，把中间结果正式纳入系统。**
