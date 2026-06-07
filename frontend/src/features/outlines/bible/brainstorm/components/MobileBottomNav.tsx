import { mobileTabs } from "../fixtures";

export interface MobileBottomNavProps {
  readonly activeTab: string;
  readonly onTabChange: (label: string) => void;
}

const TAB_BASE_CLASS =
  "flex flex-col items-center justify-center rounded px-6 py-1 transition-colors";
const ACTIVE_TAB_CLASS = `${TAB_BASE_CLASS} bg-surface-container-high text-primary-container`;
const INACTIVE_TAB_CLASS = `${TAB_BASE_CLASS} text-outline hover:bg-surface-container`;

export function MobileBottomNav({ activeTab, onTabChange }: MobileBottomNavProps) {
  return (
    <nav className="fixed bottom-0 left-1/2 z-50 flex w-full max-w-[900px] -translate-x-1/2 items-center justify-around rounded-t-lg border-t border-outline-variant bg-surface-container-low px-4 py-3 font-headline text-xs uppercase tracking-[0.12em] text-primary-container shadow-sm md:hidden">
      {mobileTabs.map((tab) => (
        <button
          className={tab.label === activeTab ? ACTIVE_TAB_CLASS : INACTIVE_TAB_CLASS}
          key={tab.label}
          onClick={() => onTabChange(tab.label)}
          type="button"
        >
          <span className="material-symbols-outlined mb-1">{tab.icon}</span>
          {tab.label}
        </button>
      ))}
    </nav>
  );
}
