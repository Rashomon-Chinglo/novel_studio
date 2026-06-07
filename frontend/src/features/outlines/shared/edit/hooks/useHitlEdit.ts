import { useState } from "react";
import type { EditActionMessages } from "../model";

type EditAction = keyof EditActionMessages;

export interface UseHitlEditOptions extends Readonly<{
  actionMessages: EditActionMessages;
}> {}

export function useHitlEdit({ actionMessages }: UseHitlEditOptions) {
  const [feedback, setFeedback] = useState("");
  const [resultMessage, setResultMessage] = useState<string>();

  function completeAction(action: EditAction) {
    setResultMessage(actionMessages[action]);
  }

  return {
    feedback,
    resultMessage,
    setFeedback,
    approve: () => completeAction("approve"),
    regenerate: () => completeAction("regenerate"),
  };
}
