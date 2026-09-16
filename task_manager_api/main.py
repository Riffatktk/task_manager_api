from fastapi import FastAPI

from database import init_db
from routes import tasks

app = FastAPI(
    title="Task Manager API",
    description=(
        "A simple, documented REST API for managing tasks — built with "
        "FastAPI + SQLite as part of Module 5 (Python Application Development)."
    ),
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(tasks.router)


@app.get("/")
def root():
    return {"message": "Task Manager API is running. Visit /docs for interactive documentation."}
