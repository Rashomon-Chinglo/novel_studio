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
    <section className="mx-auto flex w-full max-w-[800px] shrink-0 flex-col gap-4 bg-surface-bright pt-1">
      <textarea
        className="w-full resize-none border-0 border-b border-surface-container-high bg-transparent px-0 py-2 font-headline text-xl leading-relaxed text-on-surface outline-none placeholder:text-outline-variant focus:border-primary focus:ring-0"
        onChange={(e) => setDraftNote(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={brainstormBibleCopy.composerPlaceholder}
        rows={2}
        value={draftNote}
      />
      <div className="mt-2 flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap gap-4">
          <button
            className="flex items-center gap-2 rounded-full bg-primary-container px-6 py-2 font-label text-sm font-semibold text-on-primary shadow-sm transition-opacity hover:opacity-90"
            onClick={generateDraft}
            type="button"
          >
            <span className="material-symbols-outlined text-[18px]">magic_button</span>
            {brainstormBibleCopy.generateDraftLabel}
          </button>
          <button
            className="flex items-center gap-2 rounded-full border border-secondary bg-transparent px-6 py-2 font-label text-sm font-semibold text-secondary transition-colors hover:bg-surface-container"
            onClick={submitNote}
            type="button"
          >
            <span className="material-symbols-outlined text-[18px]">add_notes</span>
            {brainstormBibleCopy.addNoteLabel}
          </button>
        </div>
        <button
          className="px-4 py-2 font-label text-sm font-semibold text-outline transition-colors hover:text-error"
          onClick={clearBrainstorm}
          type="button"
        >
          {brainstormBibleCopy.clearLabel}
        </button>
      </div>
    </section>
  );
}
