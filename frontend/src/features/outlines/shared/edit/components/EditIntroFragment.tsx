export interface EditIntroFragmentProps extends Readonly<{
  title: string;
  description: string;
  version: string;
  statusMessage: string;
}> {}

export function EditIntroFragment({
  title,
  description,
  version,
  statusMessage,
}: EditIntroFragmentProps) {
  return (
    <section className="mb-8 flex flex-col gap-3">
      <h1 className="mb-2 font-headline text-[32px] font-bold text-on-surface">{title}</h1>
      <p className="font-body text-sm italic text-on-surface-variant">{description}</p>
      <div className="mt-2 flex flex-col gap-1">
        <p className="font-label text-xs uppercase tracking-wider text-on-surface-variant">
          {version}
        </p>
        <p className="font-body text-sm font-medium text-primary">{statusMessage}</p>
      </div>
    </section>
  );
}
