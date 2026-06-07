import type { EditKeyValueFragment } from "../model";
import { KeyValueFragment } from "./KeyValueFragment";

export interface KeyValueFragmentListProps extends Readonly<{
  fragments: ReadonlyArray<EditKeyValueFragment>;
}> {}

export function KeyValueFragmentList({ fragments }: KeyValueFragmentListProps) {
  return (
    <dl className="mb-10 border-b border-surface-variant">
      {fragments.map((fragment) => (
        <KeyValueFragment fragment={fragment} key={fragment.id} />
      ))}
    </dl>
  );
}
