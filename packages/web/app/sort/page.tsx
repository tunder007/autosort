/**
 * sort/page.tsx — README step 4: sort via cloud upload or CLI instructions.
 *
 * What it does:
 *   Upload zip for cloud sort; shows CLI commands for local sort.
 *
 * Input:
 *   Zip file + API key in localStorage
 *
 * Output:
 *   Cloud job + download; CLI docs for local mode
 *
 * Does not:
 *   Run OAuth or create API keys (see /connect).
 */
"use client";

import { useState } from "react";
import { api, getApiKey } from "@/lib/api";

export default function SortPage() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string>("");
  const [jobId, setJobId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function handleCloudSort() {
    if (!file) return;
    if (!getApiKey()) {
      setError("Generate an API key at /connect first");
      return;
    }

    setBusy(true);
    setError(null);
    setStatus("Creating job...");

    try {
      const job = await api.createJob("cloud");
      setJobId(job.id);
      setStatus("Uploading and sorting...");
      const done = await api.uploadZip(job.id, file);
      setStatus(`Done — ${done.files_moved} files sorted`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Sort failed");
      setStatus("");
    } finally {
      setBusy(false);
    }
  }

  async function handleDownload() {
    if (!jobId) return;
    try {
      await api.downloadJob(jobId);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Download failed");
    }
  }

  return (
    <div>
      <h1>Sort files</h1>

      <div className="card">
        <h2>Cloud</h2>
        <p>Zip the files from your folder (top-level only) and upload.</p>
        <input
          type="file"
          accept=".zip"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        <div style={{ marginTop: "1rem", display: "flex", gap: "0.5rem" }}>
          <button onClick={handleCloudSort} disabled={!file || busy}>
            {busy ? "Sorting..." : "Sort in cloud"}
          </button>
          {jobId && status.startsWith("Done") && (
            <button className="secondary" onClick={handleDownload}>
              Download result
            </button>
          )}
        </div>
        {status && <p>{status}</p>}
      </div>

      <div className="card">
        <h2>Local (CLI)</h2>
        <pre style={{ background: "#f1f5f9", padding: "1rem", borderRadius: 6, overflow: "auto" }}>
{`autosort sort "C:\\path\\to\\folder" --dry-run
autosort sort "./folder" --api-key sk_your_key`}
        </pre>
        <p>Files stay on your machine. Usage is reported to the API.</p>
      </div>

      {error && <p className="error">{error}</p>}
    </div>
  );
}
