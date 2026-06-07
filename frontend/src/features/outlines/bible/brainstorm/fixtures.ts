import type { OutlineHeaderModel } from "../../shared/layout/model";
import type { BrainstormMessage } from "./model";

export const brainstormBibleCopy = {
  clearLabel: "Clear brainstorm",
  composerPlaceholder: "继续描述世界观、主角、冲突或禁忌...",
  generateDraftLabel: "生成 Bible 初版",
} as const;

export const brainstormBibleHeader: OutlineHeaderModel = {
  segments: ["Low Whispering Forest", "New Bible Brainstorm"],
};

export const brainstormMessages: BrainstormMessage[] = [
  {
    id: "ai-opening",
    speaker: "ai",
    text: "这个故事更接近神秘、冒险、政治，还是情感创伤？",
  },
  {
    id: "author-setting",
    speaker: "author",
    text: "我想写一片能保存死者记忆的森林。",
  },
  {
    id: "ai-clarify",
    speaker: "ai",
    text: "我理解为：记忆、禁忌、继承和哀悼是核心基调。主角是否应该从个人创伤进入更大的社会秘密？",
  },
  {
    id: "author-conflict",
    speaker: "author",
    text: "是，她先寻找母亲的记忆，后来发现整个村庄都依靠这片森林维持秩序。",
  },
  {
    id: "ai-ready",
    speaker: "ai",
    text: "方向已经足够生成初版 Bible。可以继续补充，也可以让 AI 整理成结构化草稿。",
  },
];
