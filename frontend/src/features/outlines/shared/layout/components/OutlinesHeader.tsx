import type { OutlineHeaderModel } from "../model";

export interface OutlinesHeaderProps extends Readonly<{
  header?: OutlineHeaderModel;
}> {}

export function OutlinesHeader({ header }: OutlinesHeaderProps) {
  const items = header ? [...header.segments, ...(header.status ? [header.status] : [])] : [];

  return (
    <header className="sticky top-0 z-40 shrink-0 border-b border-outline-variant bg-surface/95 backdrop-blur-md">
      <div className="mx-auto flex min-h-16 w-full max-w-[960px] items-center justify-between gap-6 px-6 text-primary-container">
        <div className="shrink-0 font-headline text-xl font-bold italic tracking-tight">
          Novel Studio
        </div>

        {items.length > 0 ? (
          <nav
            aria-label="当前创作位置"
            className="flex min-w-0 items-center divide-x divide-outline-variant font-label text-sm text-outline"
          >
            {items.map((item, index) => (
              <span
                className={`max-w-52 truncate px-4 first:pl-0 last:pr-0 ${
                  index === items.length - 1 ? "font-semibold text-primary-container" : ""
                }`}
                key={`${item}-${index}`}
              >
                {item}
              </span>
            ))}
          </nav>
        ) : null}
      </div>
    </header>
  );
}
