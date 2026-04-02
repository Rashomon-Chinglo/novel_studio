# 今日任务清单

日期：2026-04-01

本文档用于定义今天这一轮最值得推进的开发任务。目标不是继续扩展零散功能，而是把当前已经存在的核心引擎往“可编排、可保存、可恢复”的应用骨架推进一步。

---

## 今日目标

今天的主任务是：

**把单章创作 workflow 所需的最小应用骨架继续补完整。**

结合当前代码和既有文档，今天不建议做：

- 前端页面
- FastAPI / SSE
- 新 Prompt 功能扩展
- 评估器
- 多用户 / 权限 / 插件化

今天建议只做 P0。

---

## P0 任务顺序

### Task 1：补 `workflow_runs` 持久化模型

目标：

- 为后续 orchestrator、错误定位、阶段恢复提供运行状态承载物。

建议落点：

- `app/persistence/models/`
- `app/persistence/repositories/workflow.py`
- `scripts/init_persistence.py` 与持久化初始化路径

建议最小字段：

- `id`
- `workflow_type`
- `status`
- `current_stage`
- `bible_id`
- `substory_id`
- `chapter_index`
- `error_code`
- `error_message`
- `started_at`
- `finished_at`

完成标准：

- 可以创建一条 chapter workflow run
- 可以更新 `status`
- 可以更新 `current_stage`
- 失败时可以记录错误信息

---

### Task 2：补 `WorkflowRunService`

目标：

- 不让未来 orchestrator 直接操作 ORM 或 repository 细节。

建议能力：

- `create_chapter_run(...)`
- `mark_stage(...)`
- `mark_succeeded(...)`
- `mark_failed(...)`
- `get(...)`

建议落点：

- `app/service/workflow.py`

完成标准：

- service 层可以独立创建和推进 run
- 上层调用不需要直接接触 `AsyncSession`

---

### Task 3：补 Post-Writing 持久化承载物

目标：

- 把 `chapter_summary` 和 `cumulative_summary` 从“纯内存结果”变成“可保存、可复用的系统对象”。

建议落点：

- `app/persistence/models/`
- `app/persistence/repositories/post_writing.py`
- `app/service/post_writing.py`

建议最小对象：

#### `chapter_summaries`

- `id`
- `workflow_run_id`
- `substory_id`
- `chapter_index`
- `content`
- `created_at`

#### `cumulative_substory_summaries`

- `id`
- `workflow_run_id`
- `substory_id`
- `content`
- `created_at`

建议 service 能力：

- `summarize_chapter(...)`
- `save_chapter_summary(...)`
- `save_cumulative_summary(...)`
- `get_latest_chapter_summary(substory_id)`
- `get_latest_cumulative_summary(substory_id)`

完成标准：

- `post_writing` 结果能落库
- 下一章可以读取最近 summary 作为输入

---

### Task 4：补 `ChapterService`

目标：

- 把 `ChapterEngine` 包成稳定的应用层接口。

建议落点：

- `app/service/outlines/chapter.py`

建议最小能力：

- `generate_blueprint(...)`
- `generate_outline(...)`
- `save_blueprint(...)`
- `save_outline(...)`
- `get(...)` 或 `get_latest_*`

注意：

- 今天可以先接受“blueprint / outline 暂存为 JSON artifact”这种简单实现
- 不必一开始就把模型拆得过细

完成标准：

- blueprint 和 outline 能分别生成
- 每一步结果都能短事务保存

---

### Task 5：补 `WritingService`

目标：

- 让正文生成拥有明确 service 边界，并可被 orchestrator 调用。

建议落点：

- `app/service/writing.py`

建议最小能力：

- `write(...)`
- `save(...)`
- `get(...)`

完成标准：

- `WritingEngine` 生成结果后可保存
- 不需要 orchestrator 直接访问 engine

---

### Task 6：实现 `ChapterOrchestrator` 的 happy path

目标：

- 先把单章流程串起来，不先追求完整恢复机制。

建议落点：

- `app/orchestrator/chapter.py`

建议最小流程：

1. 创建 `workflow_run`
2. 加载 bible / substory / latest summaries
3. 生成 blueprint 并保存
4. 生成 outline 并保存
5. 生成正文并保存
6. 生成 chapter summary 并保存
7. 生成 cumulative summary 并保存
8. 标记 run 成功

完成标准：

- 单入口能触发一轮完整章节流程
- 任一步失败时，至少能知道失败阶段

---

## 今天不要追求的事

- 不要今天就做 `resume_run`
- 不要今天就做 API 层
- 不要今天就做 streaming
- 不要今天就做复杂错误分级
- 不要今天就做完整 artifact 模型体系

今天只追求：

**把 happy path 的应用骨架立住。**

---

## 推荐执行顺序

建议按下面顺序做，不要跳着来：

1. `workflow_runs` model + repository
2. `WorkflowRunService`
3. `chapter_summary` / `cumulative_summary` model + repository + service
4. `ChapterService`
5. `WritingService`
6. `ChapterOrchestrator`
7. 对应 unit tests

原因：

- `run` 是全流程锚点
- `summary` 是下一章的重要输入
- service 边界不先立住，orchestrator 很容易变成胶水层

---

## 今日交付物

如果今天进展顺利，建议至少交付以下内容：

- `workflow_runs` 持久化落地
- `WorkflowRunService` 可用
- `PostWritingService` 可保存并读取 summary
- `ChapterService` 和 `WritingService` 初版可用
- `ChapterOrchestrator.create_chapter()` happy path 可跑
- 至少一组 service / orchestrator 测试

---

## 验收标准

今天结束前，最好能满足下面这些条件：

- 可以从单入口启动一轮 chapter workflow
- 每个关键阶段结果都不是只存在内存里
- `workflow_run.status` 和 `current_stage` 能正确推进
- 失败时能看到停在哪个阶段
- 测试不只覆盖 engine，也开始覆盖 service / orchestrator

---

## 一句话版本

今天不要再扩功能面，直接收口骨架：

**先把 workflow run、summary 持久化、service 边界和 chapter orchestrator 的 happy path 做出来。**
