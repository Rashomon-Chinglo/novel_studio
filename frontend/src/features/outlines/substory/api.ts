import { api } from "../../../api/client";

export const substoryDetailOptions = (substoryId: string) =>
  api.queryOptions("get", "/outline/substory/{substory_id}", {
    params: {
      path: {
        substory_id: substoryId,
      },
    },
  });
