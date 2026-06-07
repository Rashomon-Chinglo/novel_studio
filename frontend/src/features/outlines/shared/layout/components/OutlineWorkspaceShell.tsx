import type { ReactNode } from "react";

export interface OutlineWorkspaceShellProps extends Readonly<{
  children: ReactNode;
  footer: ReactNode;
}> {}

export function OutlineWorkspaceShell({ children, footer }: OutlineWorkspaceShellProps) {
  return (
    <div className="mx-auto flex h-full min-h-0 w-full max-w-[960px] flex-col overflow-hidden bg-background text-on-background">
      <div className="scrollbar-thin scrollbar-stable min-h-0 flex-1 overflow-y-auto">
        <main className="min-h-full px-6 py-5 pb-8">{children}</main>
      </div>
      <div className="scrollbar-stable shrink-0 overflow-y-hidden bg-surface/95 backdrop-blur-md">
        <div className="border-t border-outline-variant">{footer}</div>
      </div>
    </div>
  );
}
