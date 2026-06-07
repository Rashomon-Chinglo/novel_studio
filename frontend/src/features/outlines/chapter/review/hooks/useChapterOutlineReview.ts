import { useState } from "react";

type ReviewAction = "approve" | "defer" | "regenerate";

const ACTION_MESSAGES: Readonly<Record<ReviewAction, string>> = {
  approve: "大纲已批准，正文生成可以继续。",
  defer: "已保留当前审阅状态，你可以稍后继续。",
  regenerate: "已记录批注，准备重新生成章节大纲。",
};

export function useChapterOutlineReview() {
  const [feedback, setFeedback] = useState("");
  const [resultMessage, setResultMessage] = useState<string>();

  function completeAction(action: ReviewAction) {
    setResultMessage(ACTION_MESSAGES[action]);
  }

  return {
    feedback,
    resultMessage,
    setFeedback,
    approve: () => completeAction("approve"),
    defer: () => completeAction("defer"),
    regenerate: () => completeAction("regenerate"),
  };
}
