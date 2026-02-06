# Novel Studio 开发规范

本项目采用 **Astral 生态工具链** (`uv`, `ruff`, `ty`) 进行开发，并遵循特定的 Git 分支管理流程。

## 1. Git 分支管理与同步规范

### 核心分支
- **master**: 仅存放正式发布的稳定版本。
- **develop**: 主开发分支，汇总每日最新的开发进度。

### 每日同步 (关键)
在开始一天的工作或切换任务前，**必须执行**以下指令刷新远端状态：
```bash
git fetch --all
```
*注：`git status` 显示的 "up to date" 是基于本地缓存的远端状态。如果不在本地同步 fetch，你可能看不到别人推送的新提交。*

### 常用流程：Feature Branch Workflow

#### A. 开发小功能（1-2小时完成）
1.  **同步并创建**：`git checkout develop && git pull origin develop && git checkout -b feat/task-name`
2.  **本地开发并提交**：`git add . && git commit -m "feat: 描述"`
3.  **合并回 `develop`**：`git checkout develop && git pull origin develop && git merge feat/task-name`
4.  **推送并删除**：`git push origin develop && git branch -d feat/task-name`

#### B. 开发中/大型功能（跨天、需备份、多端协作）
1.  **创建并推送到远端**：`git checkout -b feat/big-task && git push -u origin feat/big-task`
2.  **异地/换机同步**：在另一台机器开始工作前，**必须先执行**：
    ```bash
    git fetch --all
    git checkout feat/big-task
    git pull origin feat/big-task  # 确保拉取到最新的远端代码
    ```
3.  **完成后合并**：`git checkout develop && git pull origin develop && git merge feat/big-task`
4.  **清理**：`git push origin develop && git branch -d feat/big-task && git push origin --delete feat/big-task`

---

## 2. 代码质量管控 (CI/Lint)

在提交代码前，建议运行以下指令确保代码质量。

### 代码检查与格式化 (Ruff)
- **检查并自动修复**：`uv run ruff check . --fix`
- **格式化代码**：`uv run ruff format .`

### 类型检查 (Ty)
- **运行检查**：`uv run ty check`
- *注：ty 具有极速的 LSP 支持，建议在编辑器中开启 ty 插件。*

---

## 3. IDE 环境配置 (VS Code)
- **必装插件**：`Ruff`, `Ty`, `Pylance`
- **推荐设置**：开启 "Format on Save"，并将默认 Formatter 设为 Ruff。
