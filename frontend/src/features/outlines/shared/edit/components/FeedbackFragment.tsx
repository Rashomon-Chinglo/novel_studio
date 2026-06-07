import { WorkspaceComposerInput } from "../../layout/components/WorkspaceComposerInput";
import type { EditActionLabels, EditComment } from "../model";

export interface FeedbackFragmentProps extends Readonly<{
  inputId: string;
  comments: ReadonlyArray<EditComment>;
  feedback: string;
  placeholder: string;
  resultMessage?: string;
  actionLabels: EditActionLabels;
  onFeedbackChange: (value: string) => void;
  onRegenerate: () => void;
  onApprove: () => void;
}> {}

export function FeedbackFragment({
  inputId,
  comments,
  feedback,
  placeholder,
  resultMessage,
  actionLabels,
  onFeedbackChange,
  onRegenerate,
  onApprove,
}: FeedbackFragmentProps) {
  return (
    <section className="flex w-full flex-col bg-surface-bright pt-4">
      {comments.length > 0 ? (
        <div className="flex justify-end px-6">
          <details className="group relative font-label text-xs text-on-surface-variant">
            <summary className="cursor-pointer list-none">
              已有 {comments.length} 条局部批注
            </summary>
            <div className="absolute bottom-full right-0 z-10 mb-2 w-[min(32rem,80vw)] rounded-lg border border-outline-variant bg-surface-container-lowest p-4 shadow-lg">
              {comments.map((comment) => (
                <p className="mb-2 last:mb-0" key={comment.target}>
                  <span className="mr-2 font-semibold text-primary">{comment.target}:</span>
                  <span className="font-body text-on-surface">{comment.text}</span>
                </p>
              ))}
            </div>
          </details>
        </div>
      ) : null}

      <WorkspaceComposerInput
        actions={
          <>
            <button
              aria-label={actionLabels.approve}
              className="inline-flex size-10 items-center justify-center rounded-full bg-primary-container text-on-primary shadow-sm transition-opacity hover:opacity-90"
              onClick={onApprove}
              title={actionLabels.approve}
              type="button"
            >
              <span className="material-symbols-outlined text-[20px]">magic_button</span>
            </button>
            <button
              aria-label={actionLabels.regenerate}
              className="inline-flex size-10 items-center justify-center rounded-full border border-outline-variant bg-surface-bright text-outline transition-colors hover:border-secondary hover:text-secondary"
              onClick={onRegenerate}
              title={actionLabels.regenerate}
              type="button"
            >
              <span className="material-symbols-outlined text-[20px]">refresh</span>
            </button>
          </>
        }
        ariaLabel="修改建议"
        id={inputId}
        onChange={onFeedbackChange}
        placeholder={placeholder}
        status={resultMessage}
        value={feedback}
      />
      <span aria-live="polite" className="sr-only">
        {resultMessage}
      </span>
    </section>
  );
}
