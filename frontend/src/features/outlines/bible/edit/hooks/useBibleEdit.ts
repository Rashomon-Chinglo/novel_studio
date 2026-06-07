import { useSuspenseQuery } from "@tanstack/react-query";
import { useParams } from "@tanstack/react-router";
import { useHitlEdit } from "../../../shared/edit/hooks/useHitlEdit";
import { bibleDetailOptions } from "../../api";
import { toBibleEditFragments } from "../adapters";
import { bibleEditActionMessages } from "../fixtures";

export function useBibleEdit() {
  const { bibleId } = useParams({ from: "/outlines/bible/$bibleId/edit" });
  const { data } = useSuspenseQuery(bibleDetailOptions(bibleId));
  const hitl = useHitlEdit({ actionMessages: bibleEditActionMessages });

  return {
    ...hitl,
    bibleId,
    bible: data.bible,
    fragments: toBibleEditFragments(data.bible),
  };
}
