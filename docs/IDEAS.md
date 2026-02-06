# Novel Studio - 开发思路池

本文档记录项目的零碎想法、待探索方向和潜在优化点。部分想法会逐步转化为正式的 Roadmap 项目。

---

## 测试体系完善

### 单元测试 (Unit Testing)
- **目标**：为核心模块（`writing`, `outlines`, `materials` 等）添加单元测试覆盖
- **工具**：`pytest` + Mock LLM 输出
- **优先级**：高
- **挑战**：LLM 输出的不确定性需要设计合理的 Mock 策略

### BDD 测试 (Behavior-Driven Development)
- **目标**：从用户视角验证整体创作流程（Bible → Substory → Chapter → Writing）
- **工具**：`pytest-bdd` 或 `behave`
- **场景示例**：
  - 给定一个 Bible，当执行完整流程时，应输出符合预期结构的 Chapter
  - 给定特定素材，生成的正文应包含关键要素
- **优先级**：中

---

## 流式传输 (Streaming)

### 当前问题
- 所有 LLM 输出均为一次性返回（`ainvoke`）
- 对于长文本生成（如章节创作），用户需要等待较长时间才能看到任何输出

### 改进方向
- **修改 `chain.py`**：将 `StrOutputParser` 替换为支持 Streaming 的实现
- **修改 `engine.py`**：`scene_writing` 改为 `AsyncGenerator` 或增加回调机制
- **前端适配**：需要支持 Server-Sent Events (SSE) 或 WebSocket
- **优先级**：中高
- **影响模块**：`writing`, 以及未来所有需要实时反馈的模块

---

## 评估与优化模块 (Evaluation & Continuous Improvement)

### 背景
当前系统缺乏对生成内容质量的量化评估机制，提示词优化主要依赖人工试错。

### 设计思路
1. **质量评估器 (Quality Evaluator)**
   - 使用 LLM-as-a-Judge 模式评估生成内容
   - 评估维度：情节连贯性、人物一致性、文笔质量、情感表达
   - 输出：结构化评分 + 改进建议

2. **Prompt 版本管理**
   - 记录每次 Prompt 修改历史
   - 关联生成结果的评估分数
   - 支持 A/B Testing

3. **持续优化流程**
   - 定期批量生成并评估
   - 基于评估结果自动调整 Prompt 参数
   - 可视化质量趋势

### 技术方案
- 新建 `app/modules/evaluation/` 模块
- 集成 LangSmith 或自建评估数据库
- 使用 DSPy 进行 Prompt 自动优化（探索性）

### 优先级
- 基础评估器：高
- Prompt 自动优化：中低（需要积累足够的数据）

---

## Post-Writing 模块

### 功能需求
当 `WritingEngine` 完成一个 Chapter 的创作后，需要执行一系列后处理任务：

1. **章节总结 (Chapter Summary)**
   - 当前 `engine.py` 中的 `chapter_summary` 方法为空实现
   - 需要基于生成的所有 `SceneChunk` 内容，生成精炼的章节总结
   - 用途：供后续章节创作时作为上下文

2. **更新 Substory Summary**
   - 累积当前章节的总结到 `cumulative_substory_summary`
   - 需要实现增量摘要策略（避免 Summary 无限增长）

3. **其他潜在任务**
   - **关键事件提取**：识别并记录重要剧情节点（如角色关系变化、关键道具出现）
   - **人物状态更新**：追踪角色情绪、位置、装备等状态变化
   - **冲突/悬念追踪**：记录未解决的伏笔或冲突，供后续章节参考
   - **质量自检**：调用 Evaluation 模块进行初步质量评估

### 实现建议
- 新建 `app/modules/post_writing/` 模块
- 定义 `PostWritingEngine` 类，接收 `Chapter` 和相关上下文
- 与 `WritingEngine` 解耦，通过编排层（如 `pipeline` 或 `orchestrator`）串联

### 优先级
- Chapter Summary：高（直接影响后续章节质量）
- Substory Summary 更新：高
- 关键事件提取：中
- 其他高级功能：低（可后续迭代）

---

## 其他待探索方向

### 世界观编辑器 (World Building Editor)
- 可视化管理人物关系、地点、时间线
- 自动检测矛盾（如时间线冲突、人物设定不一致）

### 多版本生成与筛选
- 对于关键章节，生成多个版本供用户选择
- 基于用户反馈训练偏好模型

### 跨语言支持
- 当前系统主要针对中文网文，未来可扩展至英文或其他语言
- 需要适配不同的文化背景和叙事风格

### 插件化架构
- 允许用户自定义 Prompt 模板、评估标准、后处理逻辑
- 建立社区生态，分享优质配置

---

## 待定想法 (Parking Lot)

- 集成语音转文字，支持口述剧情
- 生成配图建议（场景描述 → 图像提示词）
- 与游戏引擎集成，生成互动小说
