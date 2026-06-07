import {
  Outlet,
  RouterProvider,
  createRootRouteWithContext,
  createRoute,
  createRouter,
  redirect,
} from "@tanstack/react-router";
import { Suspense } from "react";
import { queryClient } from "../api/query-client";
import { BrainstormBiblePage } from "../features/outlines/bible/brainstorm/page";
import { EditBiblePage } from "../features/outlines/bible/edit/page";
import { EditChapterOutlinePage } from "../features/outlines/chapter/edit/page";
import { OutlinesLayout } from "../features/outlines/shared/layout/OutlinesLayout";
import { ErrorBoundary } from "../shared/components/ErrorBoundary";

import type { QueryClient } from "@tanstack/react-query";
import { bibleDetailOptions } from "../features/outlines/bible/api";
import { brainstormBibleHeader } from "../features/outlines/bible/brainstorm/fixtures";
import { createBibleEditHeader } from "../features/outlines/bible/edit/fixtures";
import { chapterOutlineEditHeader } from "../features/outlines/chapter/edit/fixtures";

type RouterContext = {
  queryClient: QueryClient;
};

const rootRoute = createRootRouteWithContext<RouterContext>()({
  component: RootLayout,
});

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  beforeLoad: () => {
    throw redirect({ to: "/outlines/bible/brainstorm" });
  },
});

const outlinesRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "outlines",
  component: OutlinesLayout,
});

const brainstormBibleRoute = createRoute({
  getParentRoute: () => outlinesRoute,
  path: "bible/brainstorm",
  loader: () => ({ outlineHeader: brainstormBibleHeader }),
  component: BrainstormBiblePage,
});

const editBibleRoute = createRoute({
  getParentRoute: () => outlinesRoute,
  path: "bible/$bibleId/edit",
  loader: async ({ context, params }) => {
    const bibleDetail = await context.queryClient.ensureQueryData(
      bibleDetailOptions(params.bibleId),
    );
    return { outlineHeader: createBibleEditHeader(bibleDetail.bible.title) };
  },
  component: EditBiblePage,
});

const editChapterOutlineRoute = createRoute({
  getParentRoute: () => outlinesRoute,
  path: "chapters/$chapterId/edit",
  loader: () => ({ outlineHeader: chapterOutlineEditHeader }),
  component: EditChapterOutlinePage,
});

const outlinesRouteTree = outlinesRoute.addChildren([
  brainstormBibleRoute,
  editBibleRoute,
  editChapterOutlineRoute,
]);

const routeTree = rootRoute.addChildren([indexRoute, outlinesRouteTree]);

export const router = createRouter({
  context: {
    queryClient,
  },
  routeTree,
});

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

export function AppRouter() {
  return <RouterProvider router={router} />;
}

function RootLayout() {
  return (
    <ErrorBoundary>
      <Suspense
        fallback={
          <div className="flex h-screen items-center justify-center bg-surface text-outline">
            <span className="material-symbols-outlined animate-spin text-[32px]">
              progress_activity
            </span>
          </div>
        }
      >
        <Outlet />
      </Suspense>
    </ErrorBoundary>
  );
}
