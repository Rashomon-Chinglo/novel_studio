import type { ChapterOutlineComment } from "../../../../../data/mockData";

export interface FeedbackPanelProps extends Readonly<{
  heading: string;
  comments: ReadonlyArray<ChapterOutlineComment>;
  feedback: string;
  placeholder: string;
  resultMessage?: string;
  deferLabel: string;
  regenerateLabel: string;
  approveLabel: string;
  onFeedbackChange: (value: string) => void;
  onDefer: () => void;
  onRegenerate: () => void;
  onApprove: () => void;
}> {}

export function FeedbackPanel({
  heading,
  comments,
  feedback,
  placeholder,
  resultMessage,
  deferLabel,
  regenerateLabel,
  approveLabel,
  onFeedbackChange,
  onDefer,
  onRegenerate,
  onApprove,
}: FeedbackPanelProps) {
  return (
    <section className="rounded-xl bg-surface-container-low p-6 md:p-8">
      <h3 className="mb-6 font-headline text-2xl text-on-surface">{heading}</h3>
      <div className="mb-6 flex flex-col gap-3">
        <h4 className="font-label text-xs uppercase tracking-[0.18em] text-on-surface-variant">
          Active Comments ({comments.length})
        </h4>
        {comments.map((comment) => (
          <div className="flex items-start gap-4 text-sm" key={comment.target}>
            <span className="material-symbols-outlined mt-0.5 text-[18px] text-primary">
              chat_bubble
            </span>
            <p>
              <span className="mr-2 font-label text-on-surface-variant">{comment.target}:</span>
              <span className="font-body text-on-surface">{comment.text}</span>
            </p>
          </div>
        ))}
      </div>

      <label className="sr-only" htmlFor="chapter-outline-feedback">
        整体修改建议
      </label>
      <textarea
        className="min-h-36 w-full resize-y rounded border border-surface-variant bg-surface-container-lowest p-4 font-body text-on-surface outline-none transition focus:border-outline focus:ring-1 focus:ring-outline"
        id="chapter-outline-feedback"
        onChange={(event) => onFeedbackChange(event.target.value)}
        placeholder={placeholder}
        value={feedback}
      />

      <div aria-live="polite" className="mt-3 min-h-6 font-label text-sm text-secondary">
        {resultMessage}
      </div>

      <div className="mt-5 flex flex-col-reverse gap-3 sm:flex-row sm:items-center sm:justify-end sm:gap-5">
        <button
          className="px-2 py-2 font-label text-sm text-on-surface-variant transition-colors hover:text-primary"
          onClick={onDefer}
          type="button"
        >
          {deferLabel}
        </button>
        <button
          className="rounded bg-secondary px-6 py-2.5 font-label text-sm text-on-secondary shadow-sm transition-colors hover:bg-secondary/90"
          onClick={onRegenerate}
          type="button"
        >
          {regenerateLabel}
        </button>
        <button
          className="rounded bg-gradient-to-r from-primary to-primary-container px-8 py-2.5 font-label text-sm text-on-primary shadow-sm transition-opacity hover:opacity-95"
          onClick={onApprove}
          type="button"
        >
          {approveLabel}
        </button>
      </div>
    </section>
  );
}
