import { EditIntroFragment } from "../../shared/edit/components/EditIntroFragment";
import { FeedbackFragment } from "../../shared/edit/components/FeedbackFragment";
import { KeyValueFragmentList } from "../../shared/edit/components/KeyValueFragmentList";
import { OutlineWorkspaceShell } from "../../shared/layout/components/OutlineWorkspaceShell";
import { bibleEditComments, bibleEditCopy } from "./fixtures";
import { useBibleEdit } from "./hooks/useBibleEdit";

export function EditBiblePage() {
  const edit = useBibleEdit();

  return (
    <OutlineWorkspaceShell
      footer={
        <FeedbackFragment
          actionLabels={bibleEditCopy.actionLabels}
          comments={bibleEditComments}
          feedback={edit.feedback}
          inputId="bible-feedback"
          onApprove={edit.approve}
          onFeedbackChange={edit.setFeedback}
          onRegenerate={edit.regenerate}
          placeholder={bibleEditCopy.feedbackPlaceholder}
          resultMessage={edit.resultMessage}
        />
      }
    >
      <EditIntroFragment
        description={bibleEditCopy.description}
        statusMessage={bibleEditCopy.generationStatus}
        title={bibleEditCopy.title}
        version={`${bibleEditCopy.version} · ${edit.bibleId}`}
      />

      <KeyValueFragmentList fragments={edit.fragments} />
    </OutlineWorkspaceShell>
  );
}
