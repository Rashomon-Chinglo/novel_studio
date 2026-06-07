import { useAtom, useAtomValue, useSetAtom } from "jotai";
import { draftNoteAtom, extraMessagesAtom, messagesAtom } from "../state";
import { noteSchema } from "../validation";
import { useBrainstormMutation } from "../../api";
import { useGenerateBibleDraft } from "../../api";
import { useNavigate } from "@tanstack/react-router";

export function useBrainstormBible() {
  const navigate = useNavigate();
  const [draftNote, setDraftNote] = useAtom(draftNoteAtom);
  const setExtraMessages = useSetAtom(extraMessagesAtom);
  const messages = useAtomValue(messagesAtom);
  const brainstormMutation = useBrainstormMutation();
  const generateDraftMutation = useGenerateBibleDraft();

  async function submitNote() {
    const result = noteSchema.safeParse(draftNote);
    if (!result.success) return;

    setExtraMessages((current) => [
      ...current,
      {
        id: `author-note-${crypto.randomUUID()}`,
        speaker: "author",
        text: result.data,
      },
    ]);
    setDraftNote("");

    try {
      const response = await brainstormMutation.mutateAsync({
        body: {
          user_input: result.data,
          history: messages.map((m) => m.text),
        },
      });

      setExtraMessages((current) => [
        ...current,
        {
          id: `ai-response-${crypto.randomUUID()}`,
          speaker: "ai",
          text: response.content,
        },
      ]);
    } catch {
      setExtraMessages((current) => current.slice(0, -1));
    }
  }

  function clearBrainstorm() {
    setDraftNote("");
    setExtraMessages([]);
  }

  async function generateDraft() {
    try {
      const response = await generateDraftMutation.mutateAsync({
        body: {
          messages: messages.map((m) => m.text),
        },
      });

      await navigate({
        to: "/outlines/bible/$bibleId/edit",
        params: { bibleId: response.bible_id },
      });
    } catch {}
  }

  return {
    clearBrainstorm,
    draftNote,
    messages,
    setDraftNote,
    submitNote,
    brainstormMutation,
    generateDraft,
  };
}
