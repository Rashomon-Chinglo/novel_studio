import type {
  EditActionMessages,
  EditComment,
  EditKeyValueFragment,
} from "../../shared/edit/model";
import type { OutlineHeaderModel } from "../../shared/layout/model";
import type { ChapterSceneFragmentData } from "./model";

export const chapterOutlineEditCopy = {
  title: "编辑章节大纲",
  description: "AI 已生成结构化章节大纲。你可以添加批注、写整体建议，或批准后让 AI 继续生成正文。",
  version: "ChapterOutline · Version 2 · 3 minutes ago",
  generationStatus: "正文生成已暂停，等待你确认大纲。",
  scenesHeading: "场景切分",
  feedbackPlaceholder: "输入对当前章节大纲的整体调整意见，例如：整体更克制，减少解释...",
  actionLabels: {
    regenerate: "重新生成",
    approve: "生成",
  },
} as const;

export const chapterOutlineEditHeader: OutlineHeaderModel = {
  segments: ["低语森林", "埃拉拉的冒险", "Chapter 04"],
  status: "待确认",
};

export const chapterOutlineFields: ReadonlyArray<EditKeyValueFragment> = [
  { id: "order", label: "章节序号", value: "Chapter 04 · 卷内第 2 章" },
  { id: "title", label: "章节标题", value: "守林人的秘密", tone: "strong" },
  { id: "tone", label: "章节主题色调", value: "克制、哀悼、乡土禁忌感" },
  {
    id: "opening-hook",
    label: "开头悬念",
    value: "埃拉拉在新芽中听见一段只属于母亲的摇篮曲...",
    comment: "母亲线索可以再间接一点，不要让她马上意识到真相。",
  },
  { id: "ending-hook", label: "结尾悬念", value: "她抵达心木井外..." },
];

export const chapterSceneFragments: ReadonlyArray<ChapterSceneFragmentData> = [
  {
    id: "Scene 01",
    details: [
      { label: "Location / Time", value: "寂静边缘 · 清晨" },
      { label: "Characters", value: "埃拉拉、守林人" },
      { label: "Objective", value: "让埃拉拉确认森林记忆并非幻觉", emphasized: true },
      { label: "Bridge", value: "发现母亲线索" },
    ],
    tags: ["Environment / 压抑", "Psychology / 恐惧", "Dialogue / 平静"],
  },
  {
    id: "Scene 02",
    details: [
      { label: "Location", value: "村庄" },
      { label: "Characters", value: "村长等" },
      { label: "Objective", value: "展示村庄秩序", emphasized: true },
    ],
    tags: ["Dialogue / 压抑", "Psychology / 愤怒", "Action / 平静"],
    comment: "这里的村庄禁忌感很好，但制度压力可以更具体。",
    highlighted: true,
  },
  {
    id: "Scene 03",
    details: [
      { label: "Location / Time", value: "心木井 · 夜晚" },
      { label: "Objective", value: "主动违反禁令", emphasized: true },
    ],
    tags: ["Action / 恐惧", "Image / 压抑", "Psychology / 激昂"],
  },
];

export const chapterOutlineComments: ReadonlyArray<EditComment> = [
  {
    target: "开头悬念",
    text: "母亲线索可以再间接一点，不要让她马上意识到真相。",
  },
  {
    target: "Scene 02",
    text: "这里的村庄禁忌感很好，但制度压力可以更具体。",
  },
];

export const chapterOutlineActionMessages: EditActionMessages = {
  approve: "大纲已批准，正文生成可以继续。",
  regenerate: "已记录批注，准备重新生成章节大纲。",
};
