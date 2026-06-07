import { Component } from "react";

import type { ErrorInfo, ReactNode } from "react";

export interface ErrorBoundaryProps {
  readonly children: ReactNode;
  readonly fallback?: ReactNode;
}

interface ErrorBoundaryState {
  error: Error | null;
}

/**
 * App-wide error boundary.
 *
 * Class component is still the only React-supported way to catch
 * render-phase errors (React 19 included).
 */
export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  override state: ErrorBoundaryState = { error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { error };
  }

  override componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("[ErrorBoundary]", error, info.componentStack);
  }

  override render() {
    if (this.state.error) {
      return (
        this.props.fallback ?? (
          <div className="flex h-screen flex-col items-center justify-center gap-4 bg-surface text-on-surface">
            <span className="material-symbols-outlined text-[48px] text-error">error</span>
            <h1 className="font-headline text-xl font-semibold">Something went wrong</h1>
            <p className="max-w-md text-center font-label text-sm text-outline">
              {this.state.error.message}
            </p>
            <button
              className="mt-2 rounded-full bg-primary-container px-6 py-2 font-label text-sm font-semibold text-on-primary transition-opacity hover:opacity-90"
              onClick={() => this.setState({ error: null })}
              type="button"
            >
              Try again
            </button>
          </div>
        )
      );
    }

    return this.props.children;
  }
}
