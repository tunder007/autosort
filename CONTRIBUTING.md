# Contributing to Autosort

Thank you for helping improve Autosort. This project is meant to be readable and educational — especially for learning pay-as-you-go SaaS patterns.

## Development setup

```bash
git clone https://github.com/tunder007/autosort.git
cd autosort
pip install -e ".[dev]"
pytest packages/core/tests
```

### Run the full stack locally

```bash
# API
uvicorn api.main:app --reload --port 8000

# Web (separate terminal)
cd packages/web && npm install && npm run dev
```

### Docker

```bash
docker compose up --build
```

Copy `.env.example` to `.env` and fill in GitHub/Stripe keys for OAuth and billing. See [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md).

## Documentation convention

Every Python module and every web source file should start with a module header:

```
What it does:
Input:
Output:
Does not:
```

Copy the template from [docs/MODULE_DOC_TEMPLATE.md](docs/MODULE_DOC_TEMPLATE.md).

- **Language:** English only in docs and comments.
- **Web exports:** add JSDoc (`@param`, `@returns`) on public functions in `packages/web/lib/api.ts`.
- **No scope creep:** keep changes focused; do not add features outside the README spec unless discussed in an issue.

## Tests

```bash
pytest packages/core/tests
```

Add tests in `packages/core/tests/` for algorithm changes. Name files `test_<module>.py`.

## Pull request checklist

- [ ] Module headers updated for any new or changed files
- [ ] `pytest packages/core/tests` passes
- [ ] `cd packages/web && npm run build` passes (if web changed)
- [ ] No secrets in commits (`.env`, API keys, Stripe keys)
- [ ] README or `docs/` updated if behavior or env vars change

## Architecture references

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — package layout and data flow
- [docs/SAAS_PATTERN.md](docs/SAAS_PATTERN.md) — portable pay-as-you-go pattern
