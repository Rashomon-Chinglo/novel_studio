import { expect, test } from "vite-plus/test";

import { materialSearchSchema, startChapterSchema } from "./validation";

test("materialSearchSchema sanitizes URL search params", () => {
  expect(materialSearchSchema.parse({ limit: "6", q: " 雨夜 " })).toEqual({
    limit: 6,
    q: "雨夜",
  });
});

test("startChapterSchema coerces numeric fields", () => {
  expect(
    startChapterSchema.parse({
      bible_id: "bible_1",
      chapter_index: "3",
      substory_chapter_index: "2",
      substory_id: "substory_1",
    }),
  ).toEqual({
    bible_id: "bible_1",
    chapter_index: 3,
    substory_chapter_index: 2,
    substory_id: "substory_1",
  });
});
