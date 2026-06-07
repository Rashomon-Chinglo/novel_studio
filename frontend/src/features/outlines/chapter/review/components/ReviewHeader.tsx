export interface ReviewHeaderProps extends Readonly<{
  productName: string;
  breadcrumbs: ReadonlyArray<string>;
  status: string;
}> {}

export function ReviewHeader({ productName, breadcrumbs, status }: ReviewHeaderProps) {
  return (
    <header className="mb-6 flex items-center justify-between border-b border-surface-variant py-4 md:px-10">
      <div className="flex items-center gap-4 text-on-surface">
        <svg
          aria-hidden="true"
          className="size-4 text-primary"
          fill="none"
          viewBox="0 0 48 48"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            clipRule="evenodd"
            d="M39.475 21.626c.883-.19 1.211-.067 1.283-.033.03.062.097.264.05.741-.067.692-.358 1.67-.951 2.896-1.177 2.433-3.349 5.433-6.271 8.356-2.923 2.922-5.923 5.094-8.356 6.271-1.225.593-2.205.884-2.896.951-.477.047-.679-.02-.741-.05-.034-.072-.157-.4.033-1.283.23-1.07.843-2.51 1.878-4.193 1.253-2.04 3.045-4.308 5.258-6.52 2.212-2.212 4.48-4.005 6.52-5.258 1.683-1.035 3.123-1.648 4.193-1.878ZM4.412 29.24 18.76 43.588c1.121 1.122 2.643 1.33 3.962 1.201 1.337-.13 2.793-.626 4.25-1.331 2.933-1.419 6.29-3.891 9.442-7.044 3.153-3.152 5.625-6.509 7.044-9.442.705-1.457 1.201-2.913 1.331-4.25.129-1.319-.079-2.841-1.201-3.962L29.24 4.412c-1.387-1.388-3.363-1.386-4.954-1.044-1.678.36-3.553 1.216-5.446 2.38-2.342 1.439-4.852 3.436-7.254 5.838-2.402 2.402-4.399 4.912-5.838 7.254-1.164 1.893-2.02 3.768-2.38 5.446-.342 1.591-.344 3.567 1.044 4.954Z"
            fill="currentColor"
            fillRule="evenodd"
          />
        </svg>
        <span className="font-headline text-2xl font-bold tracking-tight">{productName}</span>
      </div>

      <div className="hidden items-center gap-8 md:flex">
        <nav aria-label="章节位置" className="flex items-center gap-7 font-label text-sm">
          {breadcrumbs.map((item, index) => (
            <span className="contents" key={item}>
              {index > 0 ? <span className="text-surface-variant">/</span> : null}
              <span
                className={
                  index === breadcrumbs.length - 1
                    ? "font-bold text-on-surface"
                    : "text-on-surface-variant"
                }
              >
                {item}
              </span>
            </span>
          ))}
        </nav>
        <span className="rounded bg-primary px-4 py-2 font-label text-xs tracking-wider text-primary-fixed-dim">
          {status}
        </span>
      </div>
    </header>
  );
}
