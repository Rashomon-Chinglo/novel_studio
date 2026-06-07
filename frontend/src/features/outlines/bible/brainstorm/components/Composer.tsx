import { WorkspaceComposerInput } from "../../../shared/layout/components/WorkspaceComposerInput";
import { brainstormBibleCopy } from "../fixtures";
import { useBrainstormBible } from "../hooks/useBrainstormBible";

export function Composer() {
  const { draftNote, setDraftNote, submitNote, clearBrainstorm, generateDraft } =
    useBrainstormBible();

  function handleKeyDown(event: React.KeyboardEvent) {
    if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
      void submitNote();
    }
  }

  return (
    <section className="w-full shrink-0 bg-surface-bright pt-4">
      <WorkspaceComposerInput
        actions={
          <>
            <button
              aria-label={brainstormBibleCopy.generateDraftLabel}
              className="inline-flex size-10 items-center justify-center rounded-full bg-primary-container text-on-primary shadow-sm transition-opacity hover:opacity-90"
              onClick={generateDraft}
              title={brainstormBibleCopy.generateDraftLabel}
              type="button"
            >
              <span className="material-symbols-outlined text-[20px]">magic_button</span>
            </button>
            <button
              aria-label={brainstormBibleCopy.clearLabel}
              className="inline-flex size-10 items-center justify-center rounded-full border border-outline-variant bg-surface-bright text-outline transition-colors hover:border-error hover:text-error"
              onClick={clearBrainstorm}
              title={brainstormBibleCopy.clearLabel}
              type="button"
            >
              <span className="material-symbols-outlined text-[20px]">delete_sweep</span>
            </button>
          </>
        }
        ariaLabel={brainstormBibleCopy.composerPlaceholder}
        onChange={setDraftNote}
        onKeyDown={handleKeyDown}
        placeholder={brainstormBibleCopy.composerPlaceholder}
        value={draftNote}
      />
    </section>
  );
}
