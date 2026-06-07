import type { EditKeyValueFragment } from "../../shared/edit/model";
import { bibleFieldDefinitions } from "./fixtures";
import type { Bible } from "./model";

export function toBibleEditFragments(bible: Bible): ReadonlyArray<EditKeyValueFragment> {
  return bibleFieldDefinitions.map(({ field, label, tone }) => ({
    id: field,
    label,
    tone,
    value: bible[field],
  }));
}
