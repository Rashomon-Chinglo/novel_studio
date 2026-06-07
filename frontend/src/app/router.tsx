import {
  Outlet,
  RouterProvider,
  createRootRouteWithContext,
  createRoute,
  createRouter,
} from "@tanstack/react-router";
import { Suspense } from "react";
import { queryClient } from "../api/query-client";
import { BrainstormBiblePage } from "../features/outlines/bible/brainstorm/page";
import { EditBiblePage } from "../features/outlines/bible/edit/page";
import { ReviewChapterOutlinePage } from "../features/outlines/chapter/review/page";
import { ErrorBoundary } from "../shared/components/ErrorBoundary";

import type { QueryClient } from "@tanstack/react-query";
import { bibleDetailOptions } from "../features/outlines/bible/api";

type RouterContext = {
  queryClient: QueryClient;
};

const rootRoute = createRootRouteWithContext<RouterContext>()({
  component: RootLayout,
});

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: HomePage,
});

const brainstormBibleRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "outlines/bible/brainstorm",
  component: BrainstormBiblePage,
});

const editBibleRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "outlines/bible/$bibleId/edit",
  loader: ({ context, params }) => {
    return context.queryClient.ensureQueryData(bibleDetailOptions(params.bibleId));
  },
  component: EditBiblePage,
});

const reviewChapterOutlineRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "outlines/chapters/$chapterId/review",
  component: ReviewChapterOutlinePage,
});

const routeTree = rootRoute.addChildren([
  indexRoute,
  editBibleRoute,
  brainstormBibleRoute,
  reviewChapterOutlineRoute,
]);

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

function HomePage() {
  return <BrainstormBiblePage />;
}
