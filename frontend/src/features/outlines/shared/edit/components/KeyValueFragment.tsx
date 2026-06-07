import type { EditKeyValueFragment } from "../model";
import { InlineCommentFragment } from "./InlineCommentFragment";

export interface KeyValueFragmentProps extends Readonly<{
  fragment: EditKeyValueFragment;
}> {}

const VALUE_CLASS_BY_TONE = {
  default: "",
  emphasis: "italic",
  strong: "font-bold",
} as const;

export function KeyValueFragment({ fragment }: KeyValueFragmentProps) {
  return (
    <div className="grid gap-2 border-t border-surface-variant py-4 sm:grid-cols-[20%_1fr] sm:gap-x-6">
      <dt className="font-label text-sm text-on-surface-variant">{fragment.label}</dt>
      <dd className="flex flex-col gap-3 font-body text-[17px] text-on-surface">
        <span className={VALUE_CLASS_BY_TONE[fragment.tone ?? "default"]}>{fragment.value}</span>
        {fragment.comment ? <InlineCommentFragment text={fragment.comment} /> : null}
      </dd>
    </div>
  );
}
