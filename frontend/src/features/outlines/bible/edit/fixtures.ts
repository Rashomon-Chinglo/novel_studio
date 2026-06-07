import type { EditActionMessages, EditComment, EditValueTone } from "../../shared/edit/model";
import type { OutlineHeaderModel } from "../../shared/layout/model";
import type { BibleField } from "./model";

export interface BibleFieldDefinition {
  readonly field: BibleField;
  readonly label: string;
  readonly tone?: EditValueTone;
}

export const bibleEditCopy = {
  title: "编辑小说总纲",
  description:
    "AI 已生成小说总纲。你可以检查每个核心设定、补充整体建议，或确认后继续规划后续故事。",
  version: "Bible · Current Draft",
  generationStatus: "后续大纲生成已暂停，等待你确认小说总纲。",
  feedbackPlaceholder: "输入对当前小说总纲的整体调整意见，例如：强化主线冲突，让核心卖点更集中...",
  actionLabels: {
    regenerate: "重新生成",
    approve: "生成",
  },
} as const;

export function createBibleEditHeader(title: string): OutlineHeaderModel {
  return {
    segments: [title, "小说总纲"],
    status: "待确认",
  };
}

export const bibleFieldDefinitions: ReadonlyArray<BibleFieldDefinition> = [
  { field: "title", label: "书名", tone: "strong" },
  { field: "logline", label: "一句话梗概", tone: "emphasis" },
  { field: "marketing_hook", label: "核心卖点" },
  { field: "worldview_tone", label: "世界观基调" },
  { field: "main_conflict", label: "主线冲突" },
  { field: "ending_vision", label: "结局愿景" },
  { field: "key_roles_summary", label: "核心角色概述" },
];

export const bibleEditComments: ReadonlyArray<EditComment> = [];

export const bibleEditActionMessages: EditActionMessages = {
  approve: "总纲已在当前页面确认；后端批准接口尚未接入。",
  regenerate: "修改建议已保留；后端重生成接口尚未接入。",
};
