/**
 * connect/page.tsx — one-time onboarding (README SaaS flow).
 *
 * What it does:
 *   GitHub OAuth link, Stripe payment setup, API key generation and storage.
 *
 * Input:
 *   User clicks; session cookie from OAuth callback
 *
 * Output:
 *   API key in localStorage; usage display
 *
 * Does not:
 *   Sort files (see /sort) or show full job history (see /history).
 */
"use client";

import { useEffect, useState } from "react";
import { api, getApiKey, githubConnectUrl, setApiKey } from "@/lib/api";

export default function ConnectPage() {
  const [username, setUsername] = useState<string | null>(null);
  const [hasPayment, setHasPayment] = useState(false);
  const [usage, setUsage] = useState(0);
  const [newKey, setNewKey] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const storedKey = typeof window !== "undefined" ? getApiKey() : null;

  useEffect(() => {
    api
      .session()
      .then((s) => {
        setUsername(s.github_username);
        setHasPayment(s.has_payment_method);
        return api.usage();
      })
      .then((u) => setUsage(u.files_billed_this_month))
      .catch(() => setUsername(null))
      .finally(() => setLoading(false));
  }, []);

  async function handleBilling() {
    setError(null);
    try {
      const result = await api.setupBilling();
      if (result.dev_mode) {
        setHasPayment(true);
        return;
      }
      window.location.href = result.checkout_url;
    } catch (e) {
      setError(e instanceof Error ? e.message : "Billing setup failed");
    }
  }

  async function handleApiKey() {
    setError(null);
    try {
      const result = await api.createApiKey();
      setApiKey(result.key);
      setNewKey(result.key);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not create API key");
    }
  }

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h1>Connect</h1>
      <p>GitHub identity + payment + API key. No password accounts.</p>

      <div className="card">
        <h2>1. GitHub</h2>
        {username ? (
          <p>Connected as <strong>@{username}</strong></p>
        ) : (
          <a className="button" href={githubConnectUrl()}>
            Connect with GitHub
          </a>
        )}
      </div>

      <div className="card">
        <h2>2. Payment (pay-as-you-go)</h2>
        <p>Billed per file sorted. No subscription.</p>
        {hasPayment ? (
          <p>Payment method on file. Usage this month: <strong>{usage}</strong> files</p>
        ) : (
          <button onClick={handleBilling} disabled={!username}>
            Add payment method
          </button>
        )}
      </div>

      <div className="card">
        <h2>3. API key</h2>
        <p>Use in CLI: <code>autosort sort ./folder --api-key sk_...</code></p>
        {storedKey && !newKey && (
          <p>Stored key: <code>{storedKey.slice(0, 12)}...</code></p>
        )}
        {newKey && (
          <p>
            Copy now (shown once): <code>{newKey}</code>
          </p>
        )}
        <button onClick={handleApiKey} disabled={!username || !hasPayment}>
          Generate API key
        </button>
      </div>

      {error && <p className="error">{error}</p>}
    </div>
  );
}
