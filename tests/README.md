# tests/ 使用说明

本目录存放项目当前实际生效的测试，而不是示例测试。

---

## 当前结构

```text
tests/
├── conftest.py
├── fixtures/
├── support/
├── integration/
│   └── modules/
│       ├── outlines/
│       ├── test_materials_pipeline.py
│       ├── test_post_writing_pipeline.py
│       ├── test_outlines_pipeline.py
│       └── test_writing_pipeline.py
└── unit/
    ├── core/
    ├── db/
    ├── models/
    ├── modules/
    │   ├── base/
    │   ├── materials/
    │   ├── outlines/
    │   ├── post_writing/
    │   └── writing/
    └── service/
```

---

## 常用命令

### 全量

```bash
uv run poe test
```

### 快速

```bash
uv run poe test-quick
```

### 单元 / 集成

```bash
uv run poe test-unit
uv run poe test-integration
```

### 单文件调试

```bash
uv run pytest -p no:xdist tests/unit/modules/writing/test_engine.py -q
uv run pytest -p no:xdist tests/integration/modules/test_post_writing_pipeline.py -q
```

---

## Mock LLM 说明

测试默认通过 `tests/support/llm.py` 中的 Fake LLM 机制隔离真实模型调用。

这意味着：

- 大多数测试不需要真实 API Key 才能验证生成链路。
- 重点测试的是 prompt/context/chain 的拼装是否正确。
- 只有显式标记为 `llm` 的测试才应访问真实模型。

---

## 快照测试说明

项目使用 `inline-snapshot`。

需要注意：

- 在 `xdist` 并行模式下，快照修复功能会被禁用。
- 维护快照时请使用：

```bash
uv run poe test-fix
uv run poe test-create
```

---

## 受限环境说明

如果当前环境无法写入 `uv` 默认缓存目录，可使用：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run poe test
```

---

## 当前已知薄弱点

- `tests/unit/service/` 目前仍较空，说明 Service 层还不是稳定边界。
- API 层尚未落地，因此没有 HTTP / contract tests。
- 当未来加入 streaming 后，需要补充接口级和取消/异常路径测试。
