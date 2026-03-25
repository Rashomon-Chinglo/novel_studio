# Novel Studio 测试计划

更新日期：2026-03-25

本文档不再描述“理想中的测试体系”，而是记录当前项目已经具备的测试能力、推荐执行方式和下一步补强重点。

---

## 当前状态

截至 2026-03-25，执行：

```bash
uv run poe test
```

结果为：

- `108 passed`
- 总覆盖率 `99.20%`

这说明核心模块测试已经具备较高可用性，但还不能据此判断“工程层已经完全稳定”，因为当前覆盖重点主要集中在模块级引擎和上下文构建。

---

## 测试分层

### 1. Unit Tests

主要覆盖：

- schema 校验
- prompt 变量构建
- chain 组装
- engine 单模块行为
- context 构建逻辑

目录：

- `tests/unit/core/`
- `tests/unit/db/`
- `tests/unit/models/`
- `tests/unit/modules/`
- `tests/unit/service/`

### 2. Integration Tests

主要覆盖：

- outlines pipeline
- materials pipeline
- writing pipeline
- post-writing pipeline
- 多模块之间的上下文传递

目录：

- `tests/integration/`

### 3. 真实 LLM 测试

当前测试体系以 Mock LLM 为主，默认不依赖真实外部调用。真实模型测试后续如需引入，应明确标记为 `@pytest.mark.llm` 并与默认测试流隔离。

---

## 推荐命令

### 全量测试

```bash
uv run poe test
```

说明：

- 启用 `xdist` 并行
- 启用覆盖率统计
- 适合本地回归和 CI

### 快速验证

```bash
uv run poe test-quick
```

适合改动较小时做快速反馈。

### 分层执行

```bash
uv run poe test-unit
uv run poe test-integration
```

### 调试单文件

当你怀疑是并行执行、插件交互或快照工具影响调试时，优先使用单进程：

```bash
uv run pytest -p no:xdist tests/unit/modules/writing/test_engine.py -q
uv run pytest -p no:xdist tests/integration/modules/test_writing_pipeline.py -q
```

### 快照维护

`inline-snapshot` 在 `xdist` 下不会执行修正动作，因此维护快照时必须关闭并行：

```bash
uv run poe test-fix
uv run poe test-create
```

---

## 受限环境说明

如果运行环境对默认缓存目录有限制，可显式指定 `uv` 缓存目录：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run poe test
```

这适用于某些沙箱、CI 容器或只读家目录环境。

---

## 当前测试优势

- 核心模块不是裸测字符串，而是结合了 context、prompt 和 chain 行为。
- 已有一套可复用的 Fake LLM 机制，避免真实 API 成本。
- integration tests 已经覆盖了 `writing` 和 `post_writing` 的主流程。
- 覆盖率已经足够高，当前更需要关注“覆盖位置是否正确”。

---

## 当前测试短板

以下问题仍需补强：

1. `app/service/` 层测试明显不足，当前仍不是测试重点。
2. 应用入口、任务编排、API 层尚未成型，因此缺乏对应测试面。
3. 文档曾长期落后于实际测试目录，导致运行入口和文件路径说明不准确。
4. 快照调试、并行模式、受限环境运行方式此前没有被清晰写入文档。

---

## 下一步测试任务

### P0

- 为 `outlines` / `writing` / `post_writing` 的 Service 层补测试。
- 为未来的 orchestrator / workflow 增加集成测试。
- 在 CI 中固定 `uv run poe test`。

### P1

- 为错误处理路径补测试：
  LLM 异常、结构化输出异常、向量写入失败、数据库写入失败。
- 为流式写作增加接口测试。

### P2

- 在 API 层落地后补 contract tests。
- 当评估模块启动后，为评估输入输出增加回归测试。

---

## 提交前建议

推荐最小提交前检查：

```bash
uv run ruff check . --fix
uv run ruff format .
uv run ty check
uv run poe test-quick
```

大改动或合并前建议执行：

```bash
uv run poe test
```
