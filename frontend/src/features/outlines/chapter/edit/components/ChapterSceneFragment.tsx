import { InlineCommentFragment } from "../../../shared/edit/components/InlineCommentFragment";
import type { ChapterSceneFragmentData } from "../model";

export interface ChapterSceneFragmentProps extends Readonly<{
  scene: ChapterSceneFragmentData;
}> {}

export function ChapterSceneFragment({ scene }: ChapterSceneFragmentProps) {
  return (
    <article className="relative rounded-lg border border-surface-variant bg-surface-container-lowest p-6 shadow-[0_4px_24px_rgba(48,49,46,0.03)] [content-visibility:auto] [contain-intrinsic-size:auto_300px]">
      <span
        aria-hidden="true"
        className={`absolute -left-3 top-6 h-8 w-1 rounded-full ${
          scene.highlighted ? "bg-primary/40" : "bg-surface-variant"
        }`}
      />
      <h3 className="mb-4 font-label text-xs uppercase tracking-[0.18em] text-on-surface-variant">
        {scene.id}
      </h3>
      <dl className="mb-5 grid gap-y-3 font-body text-base sm:grid-cols-[120px_1fr]">
        {scene.details.map((detail) => (
          <div className="contents" key={detail.label}>
            <dt className="pt-1 font-label text-sm text-on-surface-variant">{detail.label}</dt>
            <dd className={detail.emphasized ? "italic text-on-surface" : "text-on-surface"}>
              {detail.value}
            </dd>
          </div>
        ))}
      </dl>
      <div className={`flex flex-wrap gap-2 ${scene.comment ? "mb-5" : ""}`}>
        {scene.tags.map((tag) => (
          <span
            className="rounded border border-secondary/20 bg-secondary/10 px-2.5 py-1 font-label text-xs text-on-secondary-container"
            key={tag}
          >
            {tag}
          </span>
        ))}
      </div>
      {scene.comment ? <InlineCommentFragment text={scene.comment} /> : null}
    </article>
  );
}
