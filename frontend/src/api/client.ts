import createFetchClient from "openapi-fetch";
import createOpenapiQueryClient from "openapi-react-query";

import type { paths } from "./schema";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "/api";

export const fetchClient = createFetchClient<paths>({
  baseUrl: apiBaseUrl,
});

export const api = createOpenapiQueryClient(fetchClient);
