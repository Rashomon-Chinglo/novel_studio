export type BrainstormMessage = Readonly<{
  id: string;
  speaker: "ai" | "author";
  text: string;
}>;

export type DirectionNote = Readonly<{
  label: string;
  value: string;
}>;

export type IconAction = Readonly<{
  icon: string;
  label: string;
}>;

export type MobileTab = Readonly<{
  icon: string;
  label: string;
}>;
