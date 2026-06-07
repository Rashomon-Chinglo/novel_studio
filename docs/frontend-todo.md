   - [ ] 1.1 更新 API 定义
       - 运行命令 pnpm api:types（确保后端服务在 8000 端口运行）。
       - 检查 src/api/schema.ts 里是否出现了 bible/create 相关类型。
   - [ ] 1.2 补全 API Hook
       - 打开 src/features/brainstorm-bible/api.ts。
       - 仿照 useBrainstormMutation，添加一个 useCreateBibleMutation
         用于生成最终大纲。
   - [ ] 1.3 强化 submitNote 逻辑
       - 打开 src/features/brainstorm-bible/hooks/useBrainstormBible.ts。
       - 把 submitNote 改为使用 try-catch 结构。
       - 确保 AI 的回复能正确追加到 extraMessagesAtom 中。

  ---

  🪜 第二阶：实现“魔法”功能 (Feature Completion)
  这一步让你的“生成大纲”按钮真正工作起来。

   - [ ] 2.1 实现 generateDraft 函数
       - 在 useBrainstormBible.ts 中，编写 generateDraft。
       - 它应该收集所有 messages 的文本，并调用 createBibleMutation。
   - [ ] 2.2 添加加载状态反馈
       - 在 Composer.tsx 中，当 mutation.isPending 为 true
         时，让按钮变灰或显示一个小转圈。
   - [ ] 2.3 清空与重置
       - 确保 clearBrainstorm 能够干净地重置所有 Atom
         状态，让用户能开启新一轮头脑风暴。
