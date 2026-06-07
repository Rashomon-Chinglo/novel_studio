import { OutlineWorkspaceShell } from "../../shared/layout/components/OutlineWorkspaceShell";
import { Composer } from "./components/Composer";
import { Conversation } from "./components/Conversation";

/**
 * BrainstormBiblePage — main page for brainstorming a story bible.
 *
 * State is managed via Jotai atoms (through hooks) for fine-grained reactivity.
 */
export function BrainstormBiblePage() {
  return (
    <div className="h-full min-h-0 font-label">
      <OutlineWorkspaceShell footer={<Composer />}>
        <Conversation />
      </OutlineWorkspaceShell>
    </div>
  );
}
