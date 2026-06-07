export interface ChapterSceneDetail {
  readonly label: string;
  readonly value: string;
  readonly emphasized?: boolean;
}

export interface ChapterSceneFragmentData {
  readonly id: string;
  readonly details: ReadonlyArray<ChapterSceneDetail>;
  readonly tags: ReadonlyArray<string>;
  readonly comment?: string;
  readonly highlighted?: boolean;
}
