export interface OutlineHeaderModel {
  readonly segments: ReadonlyArray<string>;
  readonly status?: string;
}

export interface OutlineRouteLoaderData {
  readonly outlineHeader: OutlineHeaderModel;
}
