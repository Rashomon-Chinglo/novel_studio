export interface InlineCommentProps extends Readonly<{
  text: string;
}> {}

export function InlineComment({ text }: InlineCommentProps) {
  return (
    <div className="flex w-fit gap-3 rounded-r border-l-[3px] border-primary bg-surface-container-low p-3">
      <span className="material-symbols-outlined mt-0.5 text-[18px] text-primary">comment</span>
      <p className="font-body text-sm leading-relaxed text-on-surface-variant">{text}</p>
    </div>
  );
}
