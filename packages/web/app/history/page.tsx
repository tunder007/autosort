/**
 * history/page.tsx — README step 4: job audit log viewer.
 *
 * What it does:
 *   Lists recent sort jobs from GET /history.
 *
 * Input:
 *   API key in localStorage
 *
 * Output:
 *   Table of jobs (date, mode, status, files, folder path)
 *
 * Does not:
 *   Integrate with Git; application-level audit log only.
 */
"use client";

import { useEffect, useState } from "react";
import { api, getApiKey } from "@/lib/api";

type Job = {
  id: number;
  mode: string;
  status: string;
  files_moved: number;
  folder_path: string | null;
  created_at: string;
};

export default function HistoryPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!getApiKey()) {
      setError("Set your API key at /connect first");
      return;
    }
    api
      .history()
      .then(setJobs)
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load history"));
  }, []);

  return (
    <div>
      <h1>History</h1>
      <p>Audit log of sort operations — README step 4.</p>

      {error && <p className="error">{error}</p>}

      {!error && jobs.length === 0 && <p>No jobs yet.</p>}

      {jobs.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Mode</th>
              <th>Status</th>
              <th>Files</th>
              <th>Folder</th>
            </tr>
          </thead>
          <tbody>
            {jobs.map((job) => (
              <tr key={job.id}>
                <td>{new Date(job.created_at).toLocaleString()}</td>
                <td>{job.mode}</td>
                <td>{job.status}</td>
                <td>{job.files_moved}</td>
                <td>{job.folder_path ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
