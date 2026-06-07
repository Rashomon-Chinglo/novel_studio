import type { ChapterOutlineMetadataItem } from "../../../../../data/mockData";
import { InlineComment } from "./InlineComment";

export interface OutlineMetadataProps extends Readonly<{
  items: ReadonlyArray<ChapterOutlineMetadataItem>;
}> {}

export function OutlineMetadata({ items }: OutlineMetadataProps) {
  return (
    <dl className="mb-10 border-b border-surface-variant">
      {items.map((item) => (
        <div
          className="grid gap-2 border-t border-surface-variant py-4 sm:grid-cols-[20%_1fr] sm:gap-x-6"
          key={item.label}
        >
          <dt className="font-label text-sm text-on-surface-variant">{item.label}</dt>
          <dd className="flex flex-col gap-3 font-body text-[17px] text-on-surface">
            <span className={item.emphasized ? "font-bold" : undefined}>{item.value}</span>
            {item.comment ? <InlineComment text={item.comment} /> : null}
          </dd>
        </div>
      ))}
    </dl>
  );
}
