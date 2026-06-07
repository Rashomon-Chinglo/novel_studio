import { useAtomValue } from "jotai";
import { messagesAtom } from "../state";
import { ConversationMessage } from "./ConversationMessage";

export interface ConversationProps extends Readonly<Record<string, never>> {}

export function Conversation(_: ConversationProps) {
  const messages = useAtomValue(messagesAtom);

  return (
    <section className="flex w-full flex-col gap-10">
      {messages.map((message) => (
        <ConversationMessage key={message.id} message={message} />
      ))}
    </section>
  );
}
