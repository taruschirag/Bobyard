# Comments REST API (Django + PostgreSQL) + React frontend

Simple comments service with list, create (Admin + current time), update text, and delete endpoints backed by PostgreSQL. A static React page in `../frontend/index.html` consumes the API.

## Prerequisites
- Python 3.9+
- PostgreSQL running locally and reachable on `DB_HOST`/`DB_PORT`
- curl (for quick checks)

## Backend setup (from `backend`)
1) Install Python deps:
   ```
   python3 -m pip install -r requirements.txt
   ```
2) Configure DB env vars (defaults are in `config/settings.py`; override as needed):
   ```
   export DB_NAME=bobyards
   export DB_USER=postgres
   export DB_PASSWORD=postgres
   export DB_HOST=127.0.0.1
   export DB_PORT=5432
   ```
3) Ensure the database exists (adjust user/DB names to match your setup):
   ```
   createdb bobyards
   ```
   If your Postgres user differs, create it or change the env vars above.
4) Apply migrations:
   ```
   python3 manage.py migrate
   ```
5) Seed sample data (optional but recommended):
   ```
   python3 manage.py load_comments
   ```
   Uses `data/comments_seed.json` by default; override with `--file PATH` to load a different JSON.
6) Run the API:
   ```
   python3 manage.py runserver 8000
   ```
   Base URL: `http://127.0.0.1:8000/api/comments/`

## API endpoints
- `GET /api/comments/` — list all comments (ordered by date).
- `POST /api/comments/` with JSON `{"text": "Hello world", "image": "https://..."}` — creates a comment by `Admin` with current timestamp and `likes=0`.
- `PATCH /api/comments/<id>/` with JSON `{"text": "Updated text", "image": "https://..."}` — edits comment text (and optional image).
- `DELETE /api/comments/<id>/` — removes a comment.

## Frontend (from `frontend`)
1) Serve the static page (avoid `file://` so fetch works):
   ```
   cd ../frontend
   python3 -m http.server 3000
   ```
   If 3000 is busy, pick another port, e.g., 3001.
2) Open the page: `http://localhost:3000` (or your chosen port).
3) Backend URL: update `API_BASE` near the top of `index.html` if your API isn’t at `http://127.0.0.1:8000/api/comments/`.

## CORS
`django-cors-headers` is installed and `CORS_ALLOW_ALL_ORIGINS=True` to let the frontend (different port) call the API in development. Adjust for production as needed.
