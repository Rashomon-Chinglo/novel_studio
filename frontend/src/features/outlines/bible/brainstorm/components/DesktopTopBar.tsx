import { Link } from "@tanstack/react-router";
import { brainstormBibleCopy, topBarActions } from "../fixtures";
import { IconButton } from "./IconButton";

export function DesktopTopBar() {
  return (
    <header className="sticky top-0 z-40 hidden border-b border-outline-variant bg-surface md:flex">
      <div className="mx-auto flex w-full max-w-[900px] items-center justify-between px-6 py-4 text-primary-container">
        <div className="font-headline text-xl font-bold italic tracking-tight">
          {brainstormBibleCopy.productName}
        </div>
        <nav className="flex gap-6 font-headline text-sm">
          <Link
            className="py-1 font-normal text-outline transition-colors hover:text-primary-container"
            to="/"
          >
            {brainstormBibleCopy.projectLabel}
          </Link>
          <Link
            className="border-b-2 border-primary-container py-1 font-semibold text-primary-container opacity-80 transition-opacity"
            to="/"
          >
            {brainstormBibleCopy.activeSessionLabel}
          </Link>
        </nav>
        <div className="flex gap-4">
          {topBarActions.map((action) => (
            <IconButton icon={action.icon} key={action.label} label={action.label} />
          ))}
        </div>
      </div>
    </header>
  );
}
