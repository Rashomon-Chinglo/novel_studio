import { z } from "zod";

export const noteSchema = z.string().trim().min(1);
