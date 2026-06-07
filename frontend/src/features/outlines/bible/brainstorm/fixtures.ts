import type { BrainstormMessage, DirectionNote, IconAction, MobileTab } from "./model";

export const brainstormBibleCopy = {
  activeSessionLabel: "New Bible Brainstorm",
  addNoteLabel: "Add note",
  clearLabel: "Clear brainstorm",
  composerPlaceholder: "继续描述世界观、主角、冲突或禁忌...",
  directionHeading: "当前方向",
  generateDraftLabel: "生成 Bible 初版",
  projectLabel: "Low Whispering Forest",
  productName: "Novel Studio",
} as const;

export const topBarActions: IconAction[] = [
  { icon: "settings", label: "Settings" },
  { icon: "history", label: "History" },
];

export const mobileTabs: MobileTab[] = [
  { icon: "edit_note", label: "Draft" },
  { icon: "format_list_bulleted", label: "Outline" },
  { icon: "sticky_note_2", label: "Notes" },
  { icon: "center_focus_strong", label: "Focus" },
];

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

export const directionNotes: DirectionNote[] = [
  { label: "基调", value: "神秘、哀悼、乡土禁忌" },
  { label: "核心设定", value: "森林保存死者记忆" },
  { label: "主角动机", value: "寻找母亲残留的记忆" },
  { label: "社会冲突", value: "村庄依靠森林规则维持秩序" },
];
