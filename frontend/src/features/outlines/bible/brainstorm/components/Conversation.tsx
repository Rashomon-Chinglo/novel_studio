import { useAtomValue } from "jotai";
import { messagesAtom } from "../state";
import { ConversationMessage } from "./ConversationMessage";
import { DirectionPanel } from "./DirectionPanel";
import type { DirectionNote } from "../model";

export interface ConversationProps {
  readonly directionNotes: readonly DirectionNote[];
}

export function Conversation({ directionNotes }: ConversationProps) {
  const messages = useAtomValue(messagesAtom);

  return (
    <section className="mx-auto flex min-h-0 w-full max-w-[800px] flex-1 flex-col overflow-hidden">
      <div className="scrollbar-thin flex min-h-0 flex-1 flex-col gap-10 overflow-y-auto pr-3">
        {messages.map((message) => (
          <ConversationMessage key={message.id} message={message} />
        ))}
        <DirectionPanel notes={directionNotes} />
      </div>
    </section>
  );
}
