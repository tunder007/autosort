/**
 * api.ts — HTTP client for the Autosort backend.
 *
 * What it does:
 *   Wraps fetch with API key from localStorage or session cookie for onboarding.
 *
 * Input:
 *   Env NEXT_PUBLIC_API_URL; localStorage autosort_api_key
 *
 * Output:
 *   Typed API calls and download helpers
 *
 * Does not:
 *   Run sorting logic or store secrets server-side.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Read the stored API key from browser localStorage.
 *
 * @returns API key string or null if unset / SSR
 */
export function getApiKey(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("autosort_api_key");
}

/**
 * Persist API key in localStorage for subsequent job/history requests.
 *
 * @param key - Raw sk_... key from POST /api-keys
 */
export function setApiKey(key: string): void {
  localStorage.setItem("autosort_api_key", key);
}

/**
 * Internal JSON request helper.
 *
 * @param path - API path starting with /
 * @param options - fetch init options
 * @param useSession - if true, send session cookie instead of API key
 * @returns Parsed JSON response
 */
async function request<T>(
  path: string,
  options: RequestInit = {},
  useSession = false,
): Promise<T> {
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };

  if (!useSession) {
    const apiKey = getApiKey();
    if (apiKey) headers["Authorization"] = `Bearer ${apiKey}`;
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    credentials: useSession ? "include" : "same-origin",
    headers,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || response.statusText);
  }

  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

/** Autosort API client methods grouped by domain. */
export const api = {
  /** Load GitHub session and payment status (onboarding). */
  session: () =>
    request<{ github_username: string; has_payment_method: boolean }>("/auth/session", {}, true),

  /** Create a new API key; requires GitHub session cookie. */
  createApiKey: () =>
    request<{ key: string; key_prefix: string }>(
      "/api-keys",
      { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ label: "default" }) },
      true,
    ),

  /** Start Stripe Setup Checkout or dev-mode billing. */
  setupBilling: () =>
    request<{ checkout_url: string; dev_mode?: boolean }>(
      "/billing/setup",
      { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" },
      true,
    ),

  /** Monthly file usage for current identity. */
  usage: () => request<{ files_billed_this_month: number }>("/billing/usage", {}, true),

  /**
   * Create a new sort job.
   * @param mode - "local" or "cloud"
   */
  createJob: (mode: "local" | "cloud") =>
    request<{ id: number; status: string }>("/jobs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode }),
    }),

  /**
   * Upload zip for a cloud job and wait for sort to finish.
   * @param jobId - Job id from createJob
   * @param file - Zip archive of files to sort (top-level)
   */
  uploadZip: async (jobId: number, file: File) => {
    const form = new FormData();
    form.append("file", file);
    const apiKey = getApiKey();
    const response = await fetch(`${API_URL}/jobs/${jobId}/upload`, {
      method: "POST",
      headers: apiKey ? { Authorization: `Bearer ${apiKey}` } : {},
      body: form,
    });
    if (!response.ok) throw new Error(await response.text());
    return response.json();
  },

  /** List recent jobs for audit history. */
  history: () =>
    request<
      Array<{
        id: number;
        mode: string;
        status: string;
        files_moved: number;
        folder_path: string | null;
        created_at: string;
      }>
    >("/history"),

  /**
   * Download sorted zip for a completed cloud job.
   * @param jobId - Completed cloud job id
   */
  downloadJob: async (jobId: number) => {
    const apiKey = getApiKey();
    const response = await fetch(`${API_URL}/jobs/${jobId}/download`, {
      headers: apiKey ? { Authorization: `Bearer ${apiKey}` } : {},
    });
    if (!response.ok) throw new Error(await response.text());
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `autosort_job_${jobId}.zip`;
    anchor.click();
    URL.revokeObjectURL(url);
  },
};

/**
 * URL to start GitHub OAuth (full page redirect).
 * @returns Absolute URL to GET /auth/github
 */
export function githubConnectUrl(): string {
  return `${API_URL}/auth/github`;
}
