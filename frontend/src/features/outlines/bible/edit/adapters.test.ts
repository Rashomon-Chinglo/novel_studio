import { describe, expect, test } from "vite-plus/test";
import { toBibleEditFragments } from "./adapters";

import type { Bible } from "./model";

const bible: Bible = {
  title: "雾中来信",
  logline: "一名少女追寻来自禁林的失踪者来信。",
  marketing_hook: "规则怪谈与亲情悬疑",
  worldview_tone: "潮湿、克制、民俗感",
  main_conflict: "寻找真相会不断唤醒森林。",
  ending_vision: "少女重写人与森林之间的契约。",
  key_roles_summary: "少女、守林人、失踪的母亲。",
};

describe("toBibleEditFragments", () => {
  test("maps API fields into the configured edit fragment order", () => {
    const fragments = toBibleEditFragments(bible);

    expect(fragments.map((fragment) => fragment.id)).toEqual([
      "title",
      "logline",
      "marketing_hook",
      "worldview_tone",
      "main_conflict",
      "ending_vision",
      "key_roles_summary",
    ]);
    expect(fragments[0]).toMatchObject({ label: "书名", value: "雾中来信", tone: "strong" });
    expect(fragments[6]).toMatchObject({
      label: "核心角色概述",
      value: "少女、守林人、失踪的母亲。",
    });
  });
});
