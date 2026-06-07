import type { ChapterSceneFragmentData } from "../model";
import { ChapterSceneFragment } from "./ChapterSceneFragment";

export interface ChapterScenesFragmentProps extends Readonly<{
  heading: string;
  scenes: ReadonlyArray<ChapterSceneFragmentData>;
}> {}

export function ChapterScenesFragment({ heading, scenes }: ChapterScenesFragmentProps) {
  return (
    <section aria-labelledby="chapter-scenes-heading" className="mb-12">
      <h2
        className="mb-6 inline-block border-b border-surface-container-highest pb-2 font-headline text-2xl text-on-surface"
        id="chapter-scenes-heading"
      >
        {heading}
      </h2>
      <div className="flex flex-col gap-6">
        {scenes.map((scene) => (
          <ChapterSceneFragment key={scene.id} scene={scene} />
        ))}
      </div>
    </section>
  );
}
