export interface IconButtonProps extends Readonly<{
  icon: string;
  label: string;
}> {}

export function IconButton({ icon, label }: IconButtonProps) {
  return (
    <button
      aria-label={label}
      className="inline-flex size-7 items-center justify-center text-primary-container transition-colors hover:text-primary"
      type="button"
    >
      <span className="material-symbols-outlined text-[22px]">{icon}</span>
    </button>
  );
}
