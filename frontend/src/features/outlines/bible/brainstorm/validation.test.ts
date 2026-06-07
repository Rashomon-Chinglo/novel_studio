import { expect, test } from "vite-plus/test";

import { noteSchema } from "./validation";

test("noteSchema trims whitespace and rejects empty strings", () => {
  expect(noteSchema.safeParse("  hello  ").success).toBe(true);
  expect(noteSchema.safeParse("  hello  ").data).toBe("hello");
  expect(noteSchema.safeParse("").success).toBe(false);
  expect(noteSchema.safeParse("   ").success).toBe(false);
});
