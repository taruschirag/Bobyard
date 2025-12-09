# React Comments Page

Single-page React UI that consumes the Django comments API for list/add/edit/delete as an Admin.

## Run

- Ensure backend is running and reachable at `http://localhost:8000/api/comments/` (you can change in the url in index.html) CORS is enabled in the backend settings.
- Serve the static page (so fetch works): from this folder run `python3 -m http.server 3000` and open `http://localhost:3000`.
- Alternatively open `index.html` directly, but some browsers block fetch from `file://`; .

## Backend

- Look at backend/README.md
