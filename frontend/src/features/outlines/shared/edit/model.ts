export type EditValueTone = "default" | "emphasis" | "strong";

export interface EditKeyValueFragment {
  readonly id: string;
  readonly label: string;
  readonly value: string;
  readonly tone?: EditValueTone;
  readonly comment?: string;
}

export interface EditComment {
  readonly target: string;
  readonly text: string;
}

export interface EditActionLabels {
  readonly regenerate: string;
  readonly approve: string;
}

export interface EditActionMessages {
  readonly regenerate: string;
  readonly approve: string;
}
