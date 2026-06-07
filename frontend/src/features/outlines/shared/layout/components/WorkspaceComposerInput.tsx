import type { KeyboardEventHandler, ReactNode } from "react";

export interface WorkspaceComposerInputProps extends Readonly<{
  actions: ReactNode;
  ariaLabel: string;
  id?: string;
  onChange: (value: string) => void;
  onKeyDown?: KeyboardEventHandler<HTMLTextAreaElement>;
  placeholder: string;
  rows?: number;
  status?: ReactNode;
  value: string;
}> {}

export function WorkspaceComposerInput({
  actions,
  ariaLabel,
  id,
  onChange,
  onKeyDown,
  placeholder,
  rows = 2,
  status,
  value,
}: WorkspaceComposerInputProps) {
  return (
    <div className="border-b border-surface-container-high pb-3">
      <div className="relative">
        <label className="sr-only" htmlFor={id}>
          {ariaLabel}
        </label>
        <textarea
          aria-label={id ? undefined : ariaLabel}
          className="block h-28 w-full resize-none border-0 bg-surface-container-low px-6 pb-14 pt-2 pr-28 font-headline text-xl leading-relaxed text-on-surface outline-none placeholder:text-outline-variant focus:ring-0"
          id={id}
          onChange={(event) => onChange(event.target.value)}
          onKeyDown={onKeyDown}
          placeholder={placeholder}
          rows={rows}
          value={value}
        />
        {status ? (
          <div className="absolute bottom-4 left-6 right-32 truncate font-label text-xs text-secondary">
            {status}
          </div>
        ) : null}
        <div className="absolute bottom-3 right-6 flex items-center gap-3">{actions}</div>
      </div>
    </div>
  );
}
