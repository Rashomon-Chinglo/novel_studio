import { useState } from "react";
import { Composer } from "./components/Composer";
import { Conversation } from "./components/Conversation";
import { DesktopTopBar } from "./components/DesktopTopBar";
import { MobileBottomNav } from "./components/MobileBottomNav";
import { directionNotes } from "./fixtures";

const DEFAULT_TAB = "Outline";

/**
 * BrainstormBiblePage — main page for brainstorming a story bible.
 *
 * State is managed via Jotai atoms (through hooks) for fine-grained
 * reactivity. Page-local UI state (activeTab) uses plain `useState`.
 */
export function BrainstormBiblePage() {
  const [activeTab, setActiveTab] = useState(DEFAULT_TAB);

  return (
    <div className="flex h-screen min-h-0 flex-col overflow-hidden bg-surface-bright font-label text-on-surface antialiased">
      <DesktopTopBar />
      <main className="mx-auto flex min-h-0 w-full max-w-[900px] flex-1 flex-col gap-5 px-6 pb-28 pt-6 md:pb-6">
        <Conversation directionNotes={directionNotes} />
        <Composer />
      </main>
      <MobileBottomNav activeTab={activeTab} onTabChange={setActiveTab} />
    </div>
  );
}
