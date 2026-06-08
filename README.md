# Status Check

Status Check is an MVP service for tracking commitments, deadlines, and follow-up ownership across projects and departments. The product model is intentionally calendar-first: a commitment is placed on the calendar by its deadline and represents something that should be checked by a responsible reviewer, not a task that the current user must execute themselves.

The current repository contains the backend API for the MVP: authentication, projects, commitments, status management, calendar aggregation, filtering, and database migrations.

## Product Scope

Status Check helps teams answer three operational questions:

- What commitments are due soon or already overdue?
- Who is responsible for delivering the commitment?
- Who is responsible for checking whether it was actually completed?

Commitments support the following statuses:

- `to_check` - deadline is in the future and the commitment still needs to be checked.
- `expired` - deadline has passed and the commitment was not closed or moved.
- `done` - commitment was checked and completed.
- `not_actual` - commitment is no longer relevant.
- `ideas_backlog` - commitment was moved to an ideas backlog.

## Requirements Coverage

| Requirement | Status | Implementation |
| --- | --- | --- |
| Authorization | Done | JWT-based registration and login endpoints. |
| Shared calendar | Partially done | Backend calendar endpoint groups available commitments by deadline date. A frontend calendar UI is not present in the repository. |
| Add commitment to calendar | Done | Commitments are created with a `deadline` and returned through the calendar endpoint. |
| Commitment statuses | Done | All requested statuses are represented in the domain model. |
| Edit commitment | Done | Update endpoint supports commitment field changes. |
| Change commitment status | Done | Dedicated status update endpoint. |
| Delete commitment | Done | Dedicated delete endpoint. |
| Required commitment fields | Mostly done | Author, title, description, created date, project, assignee, reviewer, and deadline are stored. API response currently returns a compact subset. |
| Calendar placement by deadline | Done | Calendar service groups commitments by `deadline.date()` and sorts by deadline time. |
| Filter by project | Done | Supported by commitments and calendar endpoints. |
| Filter by reviewer | Done | Supported by commitments endpoint. |

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy 2
- Alembic
- PostgreSQL 17
- Pydantic 2
- JWT authentication with `python-jose`
- Password hashing with Argon2 via `passlib`
- `uv` for Python dependency management
- Ruff for linting

## Project Structure

```text
.
├── backend/
│   ├── alembic/                 # Database migrations
│   ├── app/
│   │   ├── api/v1/              # HTTP routes
│   │   ├── core/                # Config and security
│   │   ├── db/                  # Session and dependencies
│   │   ├── models/              # SQLAlchemy models
│   │   ├── repositories/        # Database access layer
│   │   ├── schemas/             # Pydantic DTOs
│   │   └── services/            # Business logic
│   ├── alembic.ini
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/                    # Reserved for UI implementation
├── docker-compose.yml           # Local PostgreSQL service
└── README.md
```

## Local Setup

### 1. Start PostgreSQL

```bash
docker compose up -d db
```

The database is exposed on `localhost:5432` with these local credentials:

```text
POSTGRES_DB=status_check
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

### 2. Configure Environment

Create `backend/.env`:

```env
APP_NAME=Status Check
DEBUG=true
API_V1_PREFIX=/api/v1
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/status_check
SECRET_KEY=change-me-in-local-development
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3. Install Backend Dependencies

```bash
cd backend
uv sync
```

### 4. Run Migrations

```bash
uv run alembic upgrade head
```

### 5. Start API

```bash
uv run uvicorn app.main:app --reload
```

The API is available at:

- `http://localhost:8000`
- `http://localhost:8000/docs`
- `http://localhost:8000/db-health`

## API Overview

All protected endpoints require a bearer token:

```http
Authorization: Bearer <access_token>
```

### Auth

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
```

Register request:

```json
{
  "email": "manager@example.com",
  "username": "manager",
  "password": "strong-password"
}
```

Login request:

```json
{
  "email": "manager@example.com",
  "password": "strong-password"
}
```

### Projects

```http
POST /api/v1/projects/
GET /api/v1/projects/
```

Create project request:

```json
{
  "name": "Website Relaunch",
  "description": "Commercial site relaunch commitments"
}
```

### Commitments

```http
POST /api/v1/commitments/
GET /api/v1/commitments/?project_id=1&reviewer_id=2&status=to_check
GET /api/v1/commitments/{project_id}
PUT /api/v1/commitments/{commitment_id}
PATCH /api/v1/commitments/{commitment_id}/status?status=done
DELETE /api/v1/commitments/{commitment_id}
```

Create commitment request:

```json
{
  "title": "Send final launch estimate",
  "description": "Engineering should confirm delivery estimate before planning sync.",
  "project_id": 1,
  "assignee_id": 2,
  "reviewer_id": 3,
  "deadline": "2026-06-15T10:00:00Z"
}
```

### Calendar

```http
GET /api/v1/calendar/
GET /api/v1/calendar/?project_id=1
```

Calendar response groups commitments by deadline date:

```json
{
  "2026-06-15": [
    {
      "id": 1,
      "title": "Send final launch estimate",
      "status": "to_check",
      "project_id": 1,
      "deadline": "2026-06-15T10:00:00Z"
    }
  ]
}
```

## Domain Rules

- A commitment is visible to users who are the author, assignee, or reviewer.
- Newly created commitments start as `to_check`.
- If a commitment deadline passes and the status is not final, it resolves to `expired`.
- Final statuses are preserved by automatic status resolution: `done`, `not_actual`, and `ideas_backlog`.
- Calendar items are grouped by date and sorted by exact deadline time inside each date.

## Development Notes

Run linting:

```bash
cd backend
uv run ruff check .
```

Recommended production hardening before release:

- Add automated tests for auth, permissions, filters, deadline expiration, and calendar grouping.
- Expand commitment response schemas with all required display fields.
- Add a frontend calendar/task-tracker interface or connect this API to an existing UI.
- Add request schemas for partial updates instead of accepting raw dictionaries.
- Validate status transitions and reject unsupported status values at the API boundary.
- Add API pagination for commitment lists.
- Move local Docker credentials and secrets to environment-specific configuration.

## Current MVP Status

The backend covers the core Status Check workflow and can be used as an API-first MVP. The main missing piece for the original "web application" requirement is the frontend experience: the `frontend/` directory is currently empty, so users cannot yet manage the calendar through a browser UI inside this repository.
