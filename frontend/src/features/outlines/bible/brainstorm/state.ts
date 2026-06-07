import { atom } from "jotai";
import { brainstormMessages } from "./fixtures";
import type { BrainstormMessage } from "./model";

/**
 * Atoms for Brainstorm Bible state.
 * Using Jotai allows for fine-grained reactivity and eliminates unnecessary re-renders
 * in components that only care about a specific piece of state (e.g., the draft text).
 */

// The current text being typed in the composer
export const draftNoteAtom = atom("");

// Additional messages added during the session (not in the initial mock data)
export const extraMessagesAtom = atom<BrainstormMessage[]>([]);

// Derived atom that combines initial messages with session messages
export const messagesAtom = atom((get) => [...brainstormMessages, ...get(extraMessagesAtom)]);
