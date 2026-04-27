# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**智能日志分析与诊断平台** — A log diagnosis web platform with a FastAPI backend and static Bootstrap 5 frontend. Users submit error logs, view dashboards with charts, and get one-click AI diagnosis (rule-based engine with Claude API fallback).

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start backend (port 8001 in production, port 8000 for local dev)
cd backend
uvicorn main:app --reload --port 8000

# Frontend: open frontend/index.html directly in a browser, or serve with any static server
# NOTE: frontend/js/api.js uses port 8001 (API_BASE_URL = 'http://localhost:8001/api')
# For local dev, change to port 8000.

# Docker (production ports: backend 8000, frontend 3000)
docker-compose up --build

# Run tests
pytest tests/ -v
pytest tests/unit/ -v        # unit tests only
pytest tests/integration/ -v # integration tests only
```

## Architecture

### Backend (Python 3.11+ / FastAPI)

```
backend/
  main.py              # FastAPI app entry, CORS, global repository + diagnosis_service
  models/
    log_entry.py       # LogEntry dataclass with to_dict/from_dict
    diagnosis.py       # Diagnosis dataclass
  schemas/
    log_schemas.py     # Pydantic: LogCreate, LogUpdate, LogResponse, LogListResponse, BatchDeleteRequest
    diagnosis_schemas.py # Pydantic: DiagnosisResponse, DiagnosisCreateRequest
  repository/
    base.py            # RepositoryBase abstract interface (get, get_all, create, update, delete, delete_batch, get_stats)
    mock.py            # MockRepository — in-memory dict storage, used in production
  services/
    diagnosis_rules.py # DIAGNOSIS_RULES dict + match_rule() — keyword-based scoring
    diagnosis.py       # DiagnosisService — rule engine with LLM fallback
    diagnosis_llm.py   # call_llm() — Claude API integration (Anthropic Messages API)
  routes/
    logs.py            # POST/GET /logs, GET/PUT/DELETE /logs/{id}, DELETE /logs — supports JSON + multipart
    diagnosis.py       # POST /logs/{id}/diagnose, GET /logs/{id}/diagnosis
    dashboard.py       # GET /dashboard/stats
  utils/
    exceptions.py      # LogNotFoundError, InvalidLogDataError, DiagnosisNotFoundError, DiagnosisAlreadyExistsError
```

### Frontend (Vanilla JS + Bootstrap 5)

```
frontend/
  index.html           # Homepage (welcome page)
  submit.html          # Log submission form (text + file upload)
  list.html            # Log list with filters, pagination, batch delete
  dashboard.html       # Dashboard with Chart.js charts
  diagnosis.html       # Diagnosis detail page (log + diagnosis result)
  edit.html            # Log edit page
  404.html             # 404 error page
  500.html             # 500 error page
  css/style.css        # Custom styles
  js/
    api.js             # API wrapper (logsApi, dashboardApi, apiRequest, showToast, formatDate)
    submit.js          # Submit form logic (JSON + FormData/file upload)
    list.js            # List page (filter, paginate, view modal, delete, diagnose)
    dashboard.js       # 4 Chart.js charts (pie, bar, line, horizontal bar)
    diagnosis.js       # Diagnosis page (load log + diagnosis, render, re-diagnose)
    edit.js            # Edit page (load log, fill form, save)
```

## Key Design Decisions

- **Data layer**: `MockRepository` uses an in-memory dict (`_storage`). All data is lost on restart. The `RepositoryBase` abstract class is ready for a future DB implementation.
- **Logs route dual-mode**: `POST /api/logs` accepts both JSON (`application/json`) and `multipart/form-data` (file upload). It detects by `Content-Type` header and routes accordingly.
- **Diagnosis flow**: `DiagnosisService.diagnose()` first tries rule matching (`match_rule`). If score < 0.7 or exception type is "Other", it falls back to `call_llm()` (Claude API). If LLM also fails, it uses the rule's template/solutions.
- **LLM module**: `diagnosis_llm.py` calls the Anthropic Messages API (`httpx`). Requires `CLAUDE_API_KEY` env var. Returns `None` on failure (graceful degradation).
- **Frontend API port**: `api.js` uses `API_BASE_URL = 'http://localhost:8001/api'` (production). For local dev on 8000, change this value.
- **No build tools**: Frontend is plain HTML/JS served by nginx (Docker) or opened directly in browser. No npm/webpack/vite.

## Testing

- Tests use `pytest` with `fastapi.testclient.TestClient`.
- Integration tests use `clear_repository` fixture (autouse) to reset in-memory storage before each test.
- Unit tests use `MockRepository` with `repo.clear()` in fixtures.
- Test files:
  - `tests/unit/test_log_entry.py` — LogEntry model
  - `tests/unit/test_repository.py` — MockRepository CRUD, pagination, filters, stats
  - `tests/unit/test_diagnosis_rules.py` — Keyword matching
  - `tests/unit/test_diagnosis_service.py` — DiagnosisService flows
  - `tests/unit/test_diagnosis_llm.py` — LLM response parsing, API call mocking
  - `tests/unit/test_file_upload.py` — File parsing logic
  - `tests/integration/test_api.py` — Full API CRUD + diagnose + dashboard
  - `tests/integration/test_file_upload.py` — Multipart upload end-to-end

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/logs` | Create log (JSON or multipart/form-data with file) |
| GET | `/api/logs` | List logs (paginated, filterable) |
| GET | `/api/logs/{id}` | Get log detail |
| PUT | `/api/logs/{id}` | Update log |
| DELETE | `/api/logs/{id}` | Delete log |
| DELETE | `/api/logs` | Batch delete (body: `{ids: [...]}`) |
| POST | `/api/logs/{id}/diagnose` | Diagnose log (creates + returns) |
| GET | `/api/logs/{id}/diagnosis` | Get existing diagnosis (404 if none) |
| GET | `/api/dashboard/stats` | Dashboard statistics |

## Important Conventions

- **Severity levels**: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`
- **Exception types**: `NullPointerException`, `TimeoutError`, `DatabaseError`, `AuthenticationError`, `Other`
- **File upload**: Only `.log` and `.txt` accepted, max 5MB, UTF-8 encoding
- **Diagnosis scoring**: `match_rule` returns confidence 0.5 (no keywords) to 1.0 (multiple matches). LLM fallback triggers at < 0.7 or "Other".
- **Similar logs**: Matched by same exception_type + severity, limited to 3 results.

## Env Variables

- `CLAUDE_API_KEY` — Required for LLM fallback diagnosis
- `CLAUDE_MODEL` — Model name (default: `claude-3-5-haiku-20241022`)

## Existing Documentation

- Design spec: `docs/superpowers/specs/2026-04-23-log-diagnosis-platform-design.md`
- Implementation plan: `docs/superpowers/plans/2026-04-23-log-diagnosis-platform-plan.md`
- Missing features plan (file upload, edit page, LLM fallback, error pages — all implemented): `docs/superpowers/plans/2026-04-23-log-diagnosis-platform-missing-features.md`
