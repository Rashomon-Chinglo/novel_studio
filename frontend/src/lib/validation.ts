import { z } from "zod";

export const materialSearchSchema = z.object({
  limit: z.coerce.number().int().min(1).max(24).catch(8),
  q: z.string().trim().max(120).catch(""),
});

export const startChapterSchema = z.object({
  bible_id: z.string().trim().min(1, "需要 bible_id"),
  chapter_index: z.coerce.number().int().min(1, "章节序号必须大于 0"),
  substory_chapter_index: z.coerce.number().int().min(1, "子故事章节序号必须大于 0"),
  substory_id: z.string().trim().min(1, "需要 substory_id"),
});

export type MaterialSearch = z.infer<typeof materialSearchSchema>;
export type StartChapterInput = z.infer<typeof startChapterSchema>;
