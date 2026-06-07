export interface ChapterOutlineMetadataItem {
  readonly label: string;
  readonly value: string;
  readonly emphasized?: boolean;
  readonly comment?: string;
}

export interface ChapterOutlineSceneDetail {
  readonly label: string;
  readonly value: string;
  readonly emphasized?: boolean;
}

export interface ChapterOutlineScene {
  readonly id: string;
  readonly details: ReadonlyArray<ChapterOutlineSceneDetail>;
  readonly tags: ReadonlyArray<string>;
  readonly comment?: string;
  readonly highlighted?: boolean;
}

export interface ChapterOutlineComment {
  readonly target: string;
  readonly text: string;
}

export const chapterOutlineReviewCopy = {
  productName: "Novel Studio",
  breadcrumbs: ["低语森林", "埃拉拉的冒险", "Chapter 04"],
  status: "待审阅",
  title: "审阅章节大纲",
  description: "AI 已生成结构化章节大纲。你可以添加批注、写整体建议，或批准后让 AI 继续生成正文。",
  version: "ChapterOutline · Version 2 · 3 minutes ago",
  generationStatus: "正文生成已暂停，等待你批准大纲。",
  scenesHeading: "场景切分",
  feedbackHeading: "批注与修改建议",
  feedbackPlaceholder: "例如：整体更克制，减少解释...",
  deferAction: "稍后处理",
  regenerateAction: "带批注重生成",
  approveAction: "批准大纲",
} as const;

export const chapterOutlineMetadata: ReadonlyArray<ChapterOutlineMetadataItem> = [
  { label: "章节序号", value: "Chapter 04 · 卷内第 2 章" },
  { label: "章节标题", value: "守林人的秘密", emphasized: true },
  { label: "章节主题色调", value: "克制、哀悼、乡土禁忌感" },
  {
    label: "开头悬念",
    value: "埃拉拉在新芽中听见一段只属于母亲的摇篮曲...",
    comment: "母亲线索可以再间接一点，不要让她马上意识到真相。",
  },
  { label: "结尾悬念", value: "她抵达心木井外..." },
];

export const chapterOutlineScenes: ReadonlyArray<ChapterOutlineScene> = [
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

export const chapterOutlineComments: ReadonlyArray<ChapterOutlineComment> = [
  {
    target: "开头悬念",
    text: "母亲线索可以再间接一点，不要让她马上意识到真相。",
  },
  {
    target: "Scene 02",
    text: "这里的村庄禁忌感很好，但制度压力可以更具体。",
  },
];
