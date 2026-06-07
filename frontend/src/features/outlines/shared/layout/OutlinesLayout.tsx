import { Outlet, useMatches } from "@tanstack/react-router";
import { OutlinesHeader } from "./components/OutlinesHeader";
import type { OutlineRouteLoaderData } from "./model";

function hasOutlineHeader(value: unknown): value is OutlineRouteLoaderData {
  return typeof value === "object" && value !== null && "outlineHeader" in value;
}

export function OutlinesLayout() {
  const header = useMatches({
    select: (matches) => {
      for (let index = matches.length - 1; index >= 0; index -= 1) {
        const loaderData: unknown = matches[index]?.loaderData;
        if (hasOutlineHeader(loaderData)) return loaderData.outlineHeader;
      }
      return undefined;
    },
  });

  return (
    <div className="flex h-dvh min-h-0 flex-col overflow-hidden bg-surface-bright text-on-surface antialiased">
      <OutlinesHeader header={header} />
      <div className="min-h-0 flex-1 overflow-hidden">
        <Outlet />
      </div>
    </div>
  );
}
