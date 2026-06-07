import { EditIntroFragment } from "../../shared/edit/components/EditIntroFragment";
import { FeedbackFragment } from "../../shared/edit/components/FeedbackFragment";
import { KeyValueFragmentList } from "../../shared/edit/components/KeyValueFragmentList";
import { useHitlEdit } from "../../shared/edit/hooks/useHitlEdit";
import { OutlineWorkspaceShell } from "../../shared/layout/components/OutlineWorkspaceShell";
import { ChapterScenesFragment } from "./components/ChapterScenesFragment";
import {
  chapterOutlineActionMessages,
  chapterOutlineComments,
  chapterOutlineEditCopy,
  chapterOutlineFields,
  chapterSceneFragments,
} from "./fixtures";

export function EditChapterOutlinePage() {
  const edit = useHitlEdit({ actionMessages: chapterOutlineActionMessages });

  return (
    <OutlineWorkspaceShell
      footer={
        <FeedbackFragment
          actionLabels={chapterOutlineEditCopy.actionLabels}
          comments={chapterOutlineComments}
          feedback={edit.feedback}
          inputId="chapter-outline-feedback"
          onApprove={edit.approve}
          onFeedbackChange={edit.setFeedback}
          onRegenerate={edit.regenerate}
          placeholder={chapterOutlineEditCopy.feedbackPlaceholder}
          resultMessage={edit.resultMessage}
        />
      }
    >
      <EditIntroFragment
        description={chapterOutlineEditCopy.description}
        statusMessage={chapterOutlineEditCopy.generationStatus}
        title={chapterOutlineEditCopy.title}
        version={chapterOutlineEditCopy.version}
      />

      <KeyValueFragmentList fragments={chapterOutlineFields} />

      <ChapterScenesFragment
        heading={chapterOutlineEditCopy.scenesHeading}
        scenes={chapterSceneFragments}
      />
    </OutlineWorkspaceShell>
  );
}
