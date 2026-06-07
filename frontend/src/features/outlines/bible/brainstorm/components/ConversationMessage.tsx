import type { BrainstormMessage } from "../model";

export interface ConversationMessageProps {
  readonly message: BrainstormMessage;
}

const MESSAGE_BASE_CLASS =
  "flex flex-col gap-1 border-l-2 py-2 pl-6 [content-visibility:auto] [contain-intrinsic-size:auto_100px]";
const AUTHOR_MESSAGE_CLASS = `${MESSAGE_BASE_CLASS} ml-4 border-primary-container`;
const AI_MESSAGE_CLASS = `${MESSAGE_BASE_CLASS} border-surface-container-high`;

const META_BASE_CLASS =
  "flex items-center gap-2 font-label text-xs font-medium uppercase tracking-[0.12em]";
const AUTHOR_META_CLASS = `${META_BASE_CLASS} text-primary-container`;
const AI_META_CLASS = `${META_BASE_CLASS} text-outline`;

export function ConversationMessage({ message }: ConversationMessageProps) {
  const isAuthor = message.speaker === "author";

  return (
    <div className={isAuthor ? AUTHOR_MESSAGE_CLASS : AI_MESSAGE_CLASS}>
      <div className={isAuthor ? AUTHOR_META_CLASS : AI_META_CLASS}>
        <span className="material-symbols-outlined text-[16px]">
          {isAuthor ? "edit" : "psychology"}
        </span>
        <span>{isAuthor ? "Author" : "AI Assistant"}</span>
      </div>
      <p className="font-headline text-lg leading-relaxed text-on-surface">{message.text}</p>
    </div>
  );
}
