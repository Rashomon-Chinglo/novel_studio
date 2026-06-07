import { brainstormBibleCopy } from "../fixtures";
import type { DirectionNote } from "../model";

export interface DirectionPanelProps extends Readonly<{
  notes: ReadonlyArray<DirectionNote>;
}> {}

const EXPLORE_HEADING = (
  <div className="flex items-center gap-2 font-label text-xs font-medium uppercase tracking-[0.12em] text-secondary">
    <span className="material-symbols-outlined text-[16px]">explore</span>
    <span>{brainstormBibleCopy.directionHeading}</span>
  </div>
);

export function DirectionPanel({ notes }: DirectionPanelProps) {
  return (
    <section className="flex flex-col gap-3 border-l-2 border-secondary py-2 pl-6">
      {EXPLORE_HEADING}
      <div className="bg-surface-container-low px-5 py-4">
        <ul className="grid gap-2 font-label text-[13px] leading-[18px] text-on-surface-variant sm:grid-cols-2">
          {notes.map((note) => (
            <li className="grid grid-cols-[5rem_1fr] gap-3" key={note.label}>
              <span className="font-semibold text-on-surface">{note.label}</span>
              <span>{note.value}</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
