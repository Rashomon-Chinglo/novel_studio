export type BrainstormMessage = Readonly<{
  id: string;
  speaker: "ai" | "author";
  text: string;
}>;
