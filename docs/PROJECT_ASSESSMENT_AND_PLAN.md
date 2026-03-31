# Novel Studio 项目评估与后续开发规划

更新日期：2026-03-31

本文档基于当前仓库的真实状态整理，目标不是重复已有路线图，而是给出一份系统性的阶段评估、风险判断和后续 coding 规划。

相关文档：

- [docs/ROADMAP.md](/root/Project/cloud_workspace/novel_studio/docs/ROADMAP.md)
- [docs/ARCHITECTURE.md](/root/Project/cloud_workspace/novel_studio/docs/ARCHITECTURE.md)
- [docs/TEST_PLAN.md](/root/Project/cloud_workspace/novel_studio/docs/TEST_PLAN.md)

---

## 1. 当前阶段判断

### 结论

项目已经明显越过“从零开始的原型期”，进入：

**核心创作引擎已成型，接下来主任务是系统编排、状态管理、对外接口和工程化收口。**

换句话说，当前真正的问题不是“AI 功能不够多”，而是：

- 引擎能力还没有被稳定地串成完整 workflow
- Service 层和 Orchestrator 层还没有形成应用骨架
- 中间产物、运行状态、错误恢复和入口层仍未收口

### 当前成熟度判断

- `modules/*` 的结构已经比较清晰，`prompt / chain / context / schema / engine` 分层基本成立。
- `outlines`、`materials`、`writing`、`post_writing` 都已有可用实现。
- 测试基础较好，模块级 unit/integration 覆盖比较完整。
- 但应用层仍处于早期阶段：`main.py` 仍是占位入口，`outlines` 与 `writing` 的 service 仍未真正落地。

因此，项目当前最合理的定位不是“继续加散点能力”，而是“把已有能力收敛成稳定的创作系统”。

---

## 2. 系统性评估

### 2.1 已经做对的部分

#### A. 核心引擎边界比较健康

当前核心模块并不是一团胶水代码，而是具备较稳定的内部结构：

- `outlines` 负责 Bible、Substory、Chapter Blueprint、Chapter/Scene 生成
- `materials` 负责文本切分、素材提取、结构化输出
- `writing` 负责基于 scene blueprint、materials 和历史摘要生成正文
- `post_writing` 负责章节总结与累计总结

这意味着后续要补 `service`、`repository`、`orchestrator` 时，不需要推倒重来。

#### B. 技术栈适合当前阶段

现有组合：

- Python 3.12+
- LangChain + LangChain-OpenAI
- Pydantic v2
- SQLAlchemy + SQLite
- ChromaDB

对于当前“单机、单项目、单用户优先”的阶段，这套技术栈是够用的。短期内没有必要为了架构美感过早换栈。

#### C. 测试文化已经建立

当前仓库已经形成：

- unit tests
- integration tests
- Fake LLM 支撑
- snapshot 测试
- 分层执行命令

这是非常重要的基础资产。后面补 service、API、workflow，不会从零开始建立测试体系。

#### D. 文档开始围绕真实状态收口

`README`、`ROADMAP`、`TEST_PLAN` 和 `ARCHITECTURE` 已经开始从“理想状态描述”转向“当前真实阶段判断”，方向是正确的。

### 2.2 当前最关键的短板

#### A. 缺统一工作流编排

当前最重要的缺口是：没有一个稳定的应用级 workflow，把下面这些阶段串起来：

`Bible -> Substory -> Chapter Blueprint -> Chapter Outline -> Writing -> Summary -> Persistence`

模块能单独跑，不等于系统能稳定跑。

#### B. Service 层尚未形成稳定边界

当前只有 `materials` 有初步 service 实现，`outlines` 和 `writing` 相关 service 仍未成形。

这会导致：

- engine 层难以被稳定复用
- 上层入口无法依赖统一应用接口
- 未来 API 层容易直接穿透到底层 engine

#### C. 缺少运行状态和恢复机制

目前还没有真正的：

- workflow run
- stage status
- failure stage
- resume point
- retry policy

这会直接影响：

- 失败后的诊断
- 中断后的恢复
- 长任务 API 化
- 前端状态展示

#### D. 中间产物还不是完整的一等公民

当前 ORM 主要覆盖：

- `bibles`
- `substories`
- `chapters`
- `snippets`

但还没有系统化保存：

- chapter blueprint
- chapter outline / scene results
- chapter summary
- cumulative summary
- workflow 状态

如果只保存最终正文，就无法真正做到“可复查、可恢复、可评估”。

#### E. 错误边界和降级策略不够明确

当前还没有系统定义：

- LLM 调用失败怎么处理
- 结构化解析失败怎么处理
- SQLite 写入失败怎么处理
- Chroma 写入失败怎么处理
- 上下文过长怎么处理

其中一个关键原则必须尽快定死：

**SQLite 是主事实源，Chroma 是派生检索层。**

也就是说：

- SQL 成功、Chroma 失败，不应让主流程整体回滚
- 向量写入应允许降级，并记录待补写状态

#### F. 入口层和对外接口尚未落地

当前 `main.py` 仍是占位实现，项目还没有形成：

- CLI 入口
- API 入口
- 流式输出入口
- 任务状态查询入口

这意味着系统目前仍主要面向代码内部，而不是面向产品使用。

#### G. 工程化还没有完成闭环

目前还缺：

- CI
- 结构化日志
- 入口层测试
- service/orchestrator 测试
- API contract tests

所以现在的高覆盖率，更多说明“模块内核质量不错”，而不是“整套应用已经稳定”。

### 2.3 当前主要风险

#### A. 风险不在 Prompt 数量，而在系统骨架

如果此时继续优先扩 prompt 功能，很容易出现：

- 模块越来越多
- 编排越来越乱
- 状态越来越不可追踪
- 测试越来越偏表层

#### B. 应用层边界若不先定，后续 API 会反向污染内核

如果在 service/orchestrator 未完成前直接做 API，接口很可能绑定到底层 engine 细节，后面会非常难收口。

#### C. 存储主从关系若不尽快固定，后续会产生大量脏状态

SQLite 与 Chroma 的角色不明确时，最容易出现伪事务、补偿逻辑缺失和难以恢复的数据状态。

---

## 3. 后续 Coding 规划

### 3.1 第一优先级：完成单章创作闭环

目标：从“模块可跑”升级为“单章创作任务可稳定执行、保存、复查、恢复”。

本阶段要完成：

- 新增 Orchestrator 层，负责完整章节 workflow
- 为 `outlines`、`writing`、`post_writing` 补齐 service
- 定义阶段状态和失败边界
- 把章节总结和累计总结接入主 workflow
- 每个阶段成功后立即短事务落库

建议固定阶段顺序：

`Bible -> Substory -> ChapterBlueprint -> ChapterOutline -> Writing -> ChapterSummary -> CumulativeSummary`

### 3.2 第二优先级：补齐应用层持久化设计

目标：让中间产物、运行状态和失败信息都成为可查询对象。

建议新增或等价实现这些对象：

- `workflow_runs`
- `workflow_stage_runs`
- `chapter_blueprints`
- `chapter_outlines`
- `chapter_summaries`
- `cumulative_substory_summaries`
- `vector_sync_jobs`

设计原则：

- LLM 调用不包在长事务里
- 每阶段成功后立即提交
- SQLite 为主事实源
- Chroma 为派生索引

### 3.3 第三优先级：把 Service 层补成稳定应用边界

建议补齐这些 service：

- `BibleService`
- `SubstoryService`
- `ChapterService`
- `WritingService`
- `PostWritingService`
- `WorkflowRunService`

职责边界应明确：

- Service 负责单领域应用逻辑
- Repository 负责查询和持久化
- Orchestrator 负责跨领域流程推进
- Engine 负责 prompt、LLM 和结构化输出

### 3.4 第四优先级：补 Repository + UnitOfWork

这一步的目标不是增加抽象，而是避免 service 直接散写 ORM。

建议增加：

- `BibleRepository`
- `SubstoryRepository`
- `ChapterRepository`
- `SummaryRepository`
- `WorkflowRunRepository`
- `SnippetRepository`
- `UnitOfWork`

这样后续做恢复、幂等、重试和查询聚合时，代码会稳很多。

### 3.5 第五优先级：建立 API 与流式输出边界

等单章闭环稳定后，推荐进入 API 阶段。

默认建议：

- API 框架：FastAPI
- 长任务流式返回：SSE 优先
- 任务执行模型：先做单机异步任务，不急着上分布式队列

第一批 API 应聚焦：

- 章节生成
- workflow 状态查询
- summary 查询
- 素材导入

### 3.6 第六优先级：前端 MVP

前端不要先做重视觉和复杂交互，应只验证产品闭环。

建议 MVP 页面对齐：

- Bible 管理
- Substory 列表
- 章节生成
- 运行状态展示
- summary 查看

产品原则：

- 先可见
- 再可控
- 再可回退

### 3.7 第七优先级：评估与持续优化

评估阶段应后置，不要抢在 workflow 和 API 之前。

适合在系统边界稳定后再做：

- LLM-as-a-Judge
- 质量维度定义
- Prompt / 模型 / 输出版本化
- A/B testing
- 离线评估批处理

---

## 4. 阶段路线图

### 阶段 1：创作闭环收口

建议周期：2 到 4 周

交付目标：

- 单章 workflow 可从单入口触发
- 每阶段产物可保存
- 失败可定位到具体阶段
- 已完成阶段可复用

### 阶段 2：工程反馈系统稳定化

建议周期：1 到 2 周，可与阶段 1 部分并行

交付目标：

- service/orchestrator 测试落地
- CI 跑通
- 文档与真实状态同步
- 调试路径更清晰

### 阶段 3：API 与流式输出

建议周期：2 到 3 周

交付目标：

- 对外 API 稳定
- 章节生成支持流式输出
- 错误结构统一
- 前端无需理解内部 engine 细节

### 阶段 4：前端 MVP

建议周期：2 到 4 周

交付目标：

- 可用的最小前端闭环
- 创作过程可见
- 运行状态可观察
- 结果可查看与回溯

### 阶段 5：评估与持续优化

建议周期：系统边界稳定后再启动

交付目标：

- 建立质量反馈闭环
- 让优化从人工试错变成可追踪迭代

---

## 5. 测试与验收要求

### 必须新增的测试面

- service happy path
- orchestrator happy path
- orchestrator failure path
- resume path
- persistence path
- vector failure degraded path
- API contract path
- streaming path

### 建议验收标准

- 单章 workflow 能稳定返回 run id
- 任一阶段失败都能定位到 stage
- blueprint、outline、正文、summary 都可回查
- 默认测试不依赖真实 LLM
- 文档、命令、实际目录结构保持同步

---

## 6. 默认假设

- 当前优先目标是单用户、单机、单项目创作闭环
- 短期内继续沿用现有技术栈
- SQLite 作为主存储，Chroma 作为派生检索层
- 近期不优先做多用户、权限、插件化、复杂协作能力
- 近期不优先做大量新增 prompt 功能
- API 阶段默认采用 FastAPI + SSE

---

## 7. 一句话结论

**Novel Studio 的下一阶段，不是继续堆积新的 AI 功能，而是把已经存在的创作引擎收敛成一个稳定、可保存、可恢复、可调用、可测试的创作系统。**
