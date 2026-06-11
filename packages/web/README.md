# packages/web

Next.js UI for connect, cloud sort, and job history.

## Start

```bash
cd packages/web
npm install
npm run dev
```

Open http://localhost:3000

## Pages

| Route | Purpose |
|-------|---------|
| `/connect` | GitHub OAuth, Stripe card, API key |
| `/sort` | Upload zip (cloud) + CLI instructions |
| `/history` | Job audit log |

## Environment

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Backend URL (default `http://localhost:8000`) |

Set in `.env.local` or docker-compose. See [docs/ENVIRONMENT.md](../../docs/ENVIRONMENT.md).

## API client

All HTTP calls go through [`lib/api.ts`](lib/api.ts) with JSDoc on exported functions.
