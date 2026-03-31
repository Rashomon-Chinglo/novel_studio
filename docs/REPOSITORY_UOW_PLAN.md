# Repository 与 UnitOfWork 初版设计

更新日期：2026-03-31

本文档用于定义 Novel Studio 当前阶段的 `Repository + UnitOfWork` 初版落地方案。目标不是一次性设计完整持久化框架，而是在现有代码基础上补出一层稳定、可扩展、易测试的数据库访问边界。

相关文档：

- [ARCHITECTURE.md](/root/Project/cloud_workspace/novel_studio/docs/ARCHITECTURE.md)
- [PROJECT_ASSESSMENT_AND_PLAN.md](/root/Project/cloud_workspace/novel_studio/docs/PROJECT_ASSESSMENT_AND_PLAN.md)

---

## 1. 为什么现在要补这一层

当前仓库已经具备：

- `app/db/session.py` 中的异步 SQLAlchemy session 基础设施
- `app/models/outline.py` 中的 `Bible`、`Substory`、`Chapter`
- `app/models/snippet.py` 中的 `Snippet`
- `app/service/materials.py` 中一个早期的 service 写库示例

但当前还缺少一层明确的持久化边界，导致下面这些问题会越来越明显：

- service 层容易直接散写 `AsyncSession`
- 查询逻辑和持久化逻辑会分散在多个 service 中
- 事务边界容易不稳定
- 后续做 workflow 恢复、幂等、重试时，代码会变得难以收敛
- orchestrator 和未来 API 层容易直接依赖 ORM 细节

因此现在补 `Repository + UnitOfWork`，本质上是在为后续 service、orchestrator 和 workflow state 管理打基础。

---

## 2. 这一层要解决什么问题

### 2.1 Repository 要解决的问题

`Repository` 负责为上层提供面向业务对象的数据访问接口，而不是让 service 直接使用 ORM 查询。

它主要解决：

- 把 SQLAlchemy 查询和保存细节集中起来
- 让 service 使用更稳定的业务语义接口
- 为后续复杂查询、聚合查询、幂等检查预留统一入口

例如：

- `BibleRepository.get(bible_id)`
- `SubstoryRepository.list_by_bible(bible_id)`
- `ChapterRepository.add(chapter)`

### 2.2 UnitOfWork 要解决的问题

`UnitOfWork` 负责事务边界，而不是业务流程。

它主要解决：

- 统一管理 `AsyncSession`
- 让多个 repository 共享同一个 session
- 提供明确的 `commit` / `rollback` / `close` 生命周期
- 支撑“每个阶段成功后，立即短事务落库”的策略

在本项目中，它尤其重要，因为章节创作涉及多个 LLM 阶段，不能把整条链路包进一个长事务。

---

## 3. 职责边界

### 3.1 Repository 的职责

- 封装 SQLAlchemy 查询
- 封装 ORM 实体新增与更新
- 提供按业务语义组织的数据访问接口
- 尽量保证接口命名稳定、易理解

### 3.2 Repository 不负责

- 调用 LLM
- 编排 workflow 顺序
- 管理跨多个 service 的业务流程
- 处理长事务或重试策略

### 3.3 UnitOfWork 的职责

- 创建和持有一次 `AsyncSession`
- 暴露本次事务内可用的 repository
- 管理 `commit` / `rollback`
- 作为 service 层短事务边界

### 3.4 UnitOfWork 不负责

- 直接执行业务规则
- 决定何时调用哪个 engine
- 承担跨阶段 workflow 编排

---

## 4. 在整体架构中的位置

推荐的调用方向如下：

```text
Entry -> Orchestrator -> Service -> UnitOfWork -> Repository -> SQLAlchemy/SQLite
```

这里的关键点是：

- `Orchestrator` 负责跨阶段流程
- `Service` 负责单领域应用逻辑
- `UnitOfWork` 负责一次短事务
- `Repository` 负责持久化细节

不推荐的方式：

- service 直接到处创建 `AsyncSession`
- orchestrator 直接访问 ORM model
- 在 engine 中直接写数据库

---

## 5. 初版设计原则

### 5.1 异步优先

当前仓库的数据库基础设施是异步 SQLAlchemy，因此初版 `Repository` 和 `UnitOfWork` 也应优先采用 async 风格，避免后面再做同步到异步的迁移。

### 5.2 先小后大

初版只覆盖当前已有且最稳定的模型：

- `Bible`
- `Substory`
- `Chapter`
- `Snippet`

不在第一版引入：

- 复杂泛型 repository 基类
- 过度抽象的 query specification
- workflow run / stage run 的完整 repository 体系

### 5.3 短事务边界

必须坚持：

- LLM 调用在事务外
- 结果生成成功后，再进入 `UnitOfWork`
- 在一次短事务里完成数据库写入
- 成功后立即 `commit`

### 5.4 SQLite 是主事实源

对于 `materials` 相关场景，必须保持：

- SQLite 写入成功才算主链路成功
- 向量库是派生索引
- 不在 `UnitOfWork` 中试图把 SQLite 和 Chroma 拼成一个伪事务

---

## 6. 初版范围

今天的初版建议只落下面这些对象。

### 6.1 UnitOfWork

建议新增：

- `SqlAlchemyUnitOfWork`

建议能力：

- `__aenter__` / `__aexit__`
- `commit()`
- `rollback()`
- `session`
- `bibles`
- `substories`
- `chapters`
- `snippets`

### 6.2 Repository

建议新增：

- `BibleRepository`
- `SubstoryRepository`
- `ChapterRepository`
- `SnippetRepository`

初版接口建议控制在最小集合。

`BibleRepository`

- `get(bible_id)`
- `add(bible)`
- `list_all()`

`SubstoryRepository`

- `get(substory_id)`
- `add(substory)`
- `list_by_bible(bible_id)`

`ChapterRepository`

- `get(chapter_id)`
- `add(chapter)`
- `list_by_substory(substory_id)`

`SnippetRepository`

- `get(snippet_id)`
- `add(snippet)`
- `add_many(snippets)`
- `list_by_title(title)`

---

## 7. 推荐目录结构

初版建议将持久化相关内容统一收口到 `app/persistence/` 下：

```text
app/
├── persistence/
│   ├── db/
│   │   ├── session.py
│   │   ├── unit_of_work.py
│   │   └── vector.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── outline.py
│   │   └── snippet.py
│   └── repositories/
│       ├── __init__.py
│       ├── materials.py
│       ├── outlines/
│       │   ├── __init__.py
│       │   ├── bible.py
│       │   ├── chapter.py
│       │   └── substory.py
│       ├── post_writing.py
│       └── workflow.py
```

这样做的原因是：

- `db`、`models`、`repositories` 都属于持久化边界
- `Bible`、`Substory`、`Chapter` 明确属于 `outlines` 领域，不应平铺在 repository 根目录
- 未来继续增加 `post_writing`、`workflow`、`materials` 时，目录不会失控
- service 层会更清楚自己依赖的是“领域服务”还是“持久化能力”

---

## 8. 推荐调用方式

### 8.1 Service 中的典型写法

```python
class SomeService:
    def __init__(self, uow_factory):
        self.uow_factory = uow_factory

    async def do_something(self, payload):
        result = await self.engine.run(payload)

        async with self.uow_factory() as uow:
            uow.chapters.add(result)
            await uow.commit()

        return result
```

这里强调：

- engine 先执行
- 持久化后执行 `commit`
- 事务只包数据库写入

### 8.2 查询场景中的典型写法

```python
async with self.uow_factory() as uow:
    bible = await uow.bibles.get(bible_id)
    substories = await uow.substories.list_by_bible(bible_id)
```

如果只是读查询，初版仍可统一走 `UnitOfWork`，后续再根据性能和复杂度决定是否分出只读 query service。

---

## 9. 与现有代码的衔接建议

### 9.1 `app/service/materials.py`

这是当前最接近持久化应用层的 service。

它目前的特点是：

- 直接依赖 `AsyncSessionLocal`
- 直接构造并写入 `Snippet`
- SQL 与向量库写入放在同一个方法里

初版不建议今天立刻重构完整 `materials` 流程，但建议后续按下面方向收口：

- SQL 写入迁移到 `SnippetRepository`
- 事务交给 `SqlAlchemyUnitOfWork`
- Chroma 写入保持在 service 层，视为派生索引写入

### 9.2 `app/service/outlines/*.py` 与 `app/service/writing.py`

这些文件目前几乎为空，因此非常适合从一开始就按：

- service 依赖 `uow_factory`
- service 不直接操作 `AsyncSession`
- 持久化统一走 repository

的方式新建。

---

## 10. 今天的实施建议

今天建议按下面顺序推进。

### Step 1

先确认本文档中的：

- 职责边界
- 初版目录结构
- 初版 repository 范围

### Step 2

实现最小代码骨架：

- `app/persistence/db/unit_of_work.py`
- `app/persistence/repositories/__init__.py`
- `app/persistence/repositories/materials.py`
- `app/persistence/repositories/outlines/__init__.py`
- `app/persistence/repositories/outlines/bible.py`
- `app/persistence/repositories/outlines/substory.py`
- `app/persistence/repositories/outlines/chapter.py`

### Step 3

补最小测试，优先验证：

- repository 的基本增删查
- `UnitOfWork` 的 commit / rollback 行为

### Step 4

如果时间足够，再把 `MaterialService` 的 SQL 写入改成走 `SnippetRepository`

这一步可以作为今天的可选项，而不是必须项。

---

## 11. 暂不处理的内容

为了控制复杂度，下面这些内容明确后置：

- `WorkflowRunRepository`
- `WorkflowStageRunRepository`
- 通用 `BaseRepository[T]` 泛型体系
- 复杂筛选 DSL
- SQLite 与 Chroma 的补偿任务
- 跨聚合事务策略

这些内容会在 orchestrator 和 workflow state 真正落地后再补。

---

## 12. 一句话结论

当前阶段的 `Repository + UnitOfWork` 初版，不是为了追求抽象层数，而是为了建立一条稳定规则：

**service 负责业务，repository 负责持久化，unit of work 负责短事务。**

只要这条边界先立住，后面的 orchestrator、workflow 恢复、API 层和测试体系都会容易很多。
