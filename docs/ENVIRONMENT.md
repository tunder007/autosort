# Environment variables

Copy [`.env.example`](../.env.example) to `.env` at the repo root. Never commit `.env`.

## Database

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Prod: yes | `sqlite:///./autosort.db` | SQLAlchemy URL. Use PostgreSQL in production (`postgresql://user:pass@host:5432/autosort`). |

## GitHub OAuth (onboarding)

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_CLIENT_ID` | Prod: yes | OAuth App client ID from GitHub Developer Settings |
| `GITHUB_CLIENT_SECRET` | Prod: yes | OAuth App secret |
| `GITHUB_CALLBACK_URL` | Prod: yes | Must match GitHub app callback, e.g. `http://localhost:8000/auth/github/callback` |

Without these, `/connect` GitHub button returns 503. Local CLI sorting still works.

## Session

| Variable | Required | Description |
|----------|----------|-------------|
| `SESSION_SECRET` | Prod: yes | Random string for signing onboarding session cookies |

## Stripe (pay-as-you-go billing)

| Variable | Required | Description |
|----------|----------|-------------|
| `STRIPE_SECRET_KEY` | Prod: yes | Stripe secret key (`sk_test_` or `sk_live_`) |
| `STRIPE_WEBHOOK_SECRET` | Optional | For webhook verification if you add Stripe webhooks later |
| `STRIPE_METER_EVENT_NAME` | Optional | Meter event name in Stripe Billing (default: `autosort_files`) |
| `STRIPE_PRICE_ID` | Optional | Reserved for future price configuration |
| `PRICE_PER_FILE_CENTS` | Optional | Documented list price per file (default: `0.1`); meter config is in Stripe dashboard |

Without `STRIPE_SECRET_KEY`, billing runs in **dev mode**: local usage counter only, fake `dev_cus_*` customer IDs.

## URLs

| Variable | Required | Description |
|----------|----------|-------------|
| `WEB_URL` | Prod: yes | Frontend origin for OAuth redirects and CORS, e.g. `http://localhost:3000` |
| `API_URL` | Prod: yes | Public API base URL |
| `NEXT_PUBLIC_API_URL` | Web build | Same as API URL; baked into Next.js client |

## Storage

| Variable | Required | Description |
|----------|----------|-------------|
| `STORAGE_PATH` | Optional | Directory for cloud job zips (default: `./packages/api/storage`) |

## Minimal local dev (no OAuth/Stripe)

```env
DATABASE_URL=sqlite:///./autosort.db
SESSION_SECRET=dev-secret
WEB_URL=http://localhost:3000
API_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Use `autosort sort ./folder` without API key. SaaS features need GitHub + Stripe for full flow.

## Docker Compose

`docker-compose.yml` sets `DATABASE_URL`, `WEB_URL`, `API_URL`, and `STORAGE_PATH` for the `api` service. Add GitHub and Stripe via env file or compose overrides for production-like testing.
