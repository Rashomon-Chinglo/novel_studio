import { api } from "../../../api/client";

export function useBrainstormMutation() {
  return api.useMutation("post", "/outline/bible/brainstorm");
}

export function useGenerateBibleDraft() {
  return api.useMutation("post", "/outline/bible/create");
}

export const bibleDetailOptions = (bibleId: string) =>
  api.queryOptions("get", "/outline/bible/{bible_id}", {
    params: {
      path: {
        bible_id: bibleId,
      },
    },
  });
