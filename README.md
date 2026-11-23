# DevTrack

DevTrack is a small project and task tracker for keeping coursework, side projects, and personal builds in one place. It started as a simple way to see what needs doing without opening five different apps.

## What it does

- Create projects and keep related tasks together.
- Move tasks between To do, Doing, and Done.
- Set a priority, search your task list, and filter by status.
- See a quick count of projects, open tasks, and completed work.
- Keep tasks when deleting a project; they become unassigned instead of disappearing.

## Built with

- **Frontend:** React, Vite, and plain CSS
- **Backend:** Python, FastAPI, and SQLAlchemy
- **Database:** SQLite by default

## Run it locally

You will need Python 3.10+ and Node.js 20+.

### 1. Start the API

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at http://127.0.0.1:8000. Interactive API docs are at http://127.0.0.1:8000/docs.

### 2. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite serves the app at http://localhost:5173 and forwards `/api` requests to the backend.

## Run the backend tests

From the `backend` directory:

```bash
pip install -r requirements.txt
pip install pytest httpx
pytest -q
```

## API routes

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Check that the API is up |
| GET | `/api/dashboard` | Dashboard counts |
| GET / POST | `/api/projects` | List or create projects |
| DELETE | `/api/projects/{id}` | Remove a project without removing its tasks |
| GET / POST | `/api/tasks` | List or create tasks |
| PATCH / DELETE | `/api/tasks/{id}` | Update or remove a task |

## Current scope

This is an early single-user version. There is no login, cloud database, team sharing, or deployment setup yet. SQLite data stays on the machine running the API.
