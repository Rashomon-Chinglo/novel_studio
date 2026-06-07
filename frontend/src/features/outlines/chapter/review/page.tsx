import {
  chapterOutlineComments,
  chapterOutlineMetadata,
  chapterOutlineReviewCopy,
  chapterOutlineScenes,
} from "../../../../data/mockData";
import { FeedbackPanel } from "./components/FeedbackPanel";
import { OutlineMetadata } from "./components/OutlineMetadata";
import { ReviewHeader } from "./components/ReviewHeader";
import { SceneCard } from "./components/SceneCard";
import { useChapterOutlineReview } from "./hooks/useChapterOutlineReview";

export function ReviewChapterOutlinePage() {
  const review = useChapterOutlineReview();

  return (
    <div className="min-h-screen overflow-x-hidden bg-background text-on-background antialiased">
      <div className="mx-auto flex w-full max-w-[1280px] justify-center px-4 py-5 md:px-10 lg:px-40">
        <div className="w-full max-w-[960px]">
          <ReviewHeader
            breadcrumbs={chapterOutlineReviewCopy.breadcrumbs}
            productName={chapterOutlineReviewCopy.productName}
            status={chapterOutlineReviewCopy.status}
          />

          <main className="pb-20 md:px-10">
            <section className="mb-8 flex flex-col gap-3">
              <h1 className="mb-2 font-headline text-[32px] font-bold text-on-surface">
                {chapterOutlineReviewCopy.title}
              </h1>
              <p className="font-body text-sm italic text-on-surface-variant">
                {chapterOutlineReviewCopy.description}
              </p>
              <div className="mt-2 flex flex-col gap-1">
                <p className="font-label text-xs uppercase tracking-wider text-on-surface-variant">
                  {chapterOutlineReviewCopy.version}
                </p>
                <p className="font-body text-sm font-medium text-primary">
                  {chapterOutlineReviewCopy.generationStatus}
                </p>
              </div>
            </section>

            <OutlineMetadata items={chapterOutlineMetadata} />

            <section aria-labelledby="scenes-heading" className="mb-12">
              <h2
                className="mb-6 inline-block border-b border-surface-container-highest pb-2 font-headline text-2xl text-on-surface"
                id="scenes-heading"
              >
                {chapterOutlineReviewCopy.scenesHeading}
              </h2>
              <div className="flex flex-col gap-6">
                {chapterOutlineScenes.map((scene) => (
                  <SceneCard key={scene.id} scene={scene} />
                ))}
              </div>
            </section>

            <FeedbackPanel
              approveLabel={chapterOutlineReviewCopy.approveAction}
              comments={chapterOutlineComments}
              deferLabel={chapterOutlineReviewCopy.deferAction}
              feedback={review.feedback}
              heading={chapterOutlineReviewCopy.feedbackHeading}
              onApprove={review.approve}
              onDefer={review.defer}
              onFeedbackChange={review.setFeedback}
              onRegenerate={review.regenerate}
              placeholder={chapterOutlineReviewCopy.feedbackPlaceholder}
              regenerateLabel={chapterOutlineReviewCopy.regenerateAction}
              resultMessage={review.resultMessage}
            />
          </main>
        </div>
      </div>
    </div>
  );
}
