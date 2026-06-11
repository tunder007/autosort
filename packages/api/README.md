# packages/api

FastAPI backend — pay-as-you-go SaaS layer around the core sorter.

## Start

```bash
pip install -e .
uvicorn api.main:app --reload --port 8000
```

- Health: http://localhost:8000/health  
- OpenAPI: http://localhost:8000/docs  

## Routers

| File | Prefix | Purpose |
|------|--------|---------|
| `github.py` | `/auth` | GitHub OAuth + session |
| `api_keys.py` | `/api-keys` | Generate keys (GitHub session required) |
| `billing.py` | `/billing` | Stripe setup + usage |
| `jobs.py` | `/jobs` | Create, complete, download jobs |
| `upload.py` | `/jobs/{id}/upload` | Cloud zip upload |
| `history.py` | `/history` | Job audit log |

## Authentication model

| Use case | Mechanism |
|----------|-----------|
| Onboarding (`/connect`) | `autosort_session` cookie after GitHub OAuth |
| Jobs, history, upload | `Authorization: Bearer sk_...` |

No email/password accounts. See [docs/SAAS_PATTERN.md](../../docs/SAAS_PATTERN.md).

## Environment

See [docs/ENVIRONMENT.md](../../docs/ENVIRONMENT.md).
