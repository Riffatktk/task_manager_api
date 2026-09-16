# Task Manager API

A fully documented REST API for managing tasks, built with **FastAPI** and **SQLite** —
covers routing, CRUD via raw SQL, request/response validation with Pydantic, and
simple API-key authentication.

## Project structure

```
task_manager_api/
├── main.py            # App entry point, mounts routers
├── database.py         # SQLite connection + table setup
├── schemas.py           # Pydantic request/response models
├── auth.py               # API key authentication
├── routes/
│   ├── __init__.py
│   └── tasks.py            # CRUD endpoints for tasks
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`.
Interactive, auto-generated docs (Swagger UI) are at `http://127.0.0.1:8000/docs`.

## Authentication

Every `/tasks` endpoint requires an API key header:

```
X-API-Key: supersecret-api-key-123
```

(In a real project, load this from an environment variable instead of hardcoding it.)

## Endpoints

| Method | Path           | Description         | Auth required |
|--------|----------------|----------------------|:---:|
| GET    | `/`            | Health check          | No |
| POST   | `/tasks/`      | Create a task          | Yes |
| GET    | `/tasks/`      | List all tasks          | Yes |
| GET    | `/tasks/{id}`  | Get a single task        | Yes |
| PUT    | `/tasks/{id}`  | Update a task (partial)   | Yes |
| DELETE | `/tasks/{id}`  | Delete a task              | Yes |

## Example requests

**Create a task**
```bash
curl -X POST http://127.0.0.1:8000/tasks/ \
  -H "X-API-Key: supersecret-api-key-123" \
  -H "Content-Type: application/json" \
  -d '{"title": "Finish Module 5", "description": "Build the REST API", "completed": false}'
```

**List tasks**
```bash
curl http://127.0.0.1:8000/tasks/ -H "X-API-Key: supersecret-api-key-123"
```

**Update a task**
```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "X-API-Key: supersecret-api-key-123" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

**Delete a task**
```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1 -H "X-API-Key: supersecret-api-key-123"
```

## What this project demonstrates

- FastAPI routing, path params, request bodies, and dependency injection
- SQLite database setup and CRUD operations using raw SQL
- Request/response validation and auto-generated OpenAPI docs via Pydantic
- Basic API-key authentication applied per-endpoint
