from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from auth import verify_api_key
from database import get_db
from schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
def create_task(task: TaskCreate):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
            (task.title, task.description, task.completed),
        )
        db.commit()
        task_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return dict(row)


@router.get(
    "/",
    response_model=List[TaskResponse],
    dependencies=[Depends(verify_api_key)],
)
def list_tasks():
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    dependencies=[Depends(verify_api_key)],
)
def get_task(task_id: int):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return dict(row)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    dependencies=[Depends(verify_api_key)],
)
def update_task(task_id: int, task: TaskUpdate):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        existing = cursor.fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Task not found")

        updated_fields = task.dict(exclude_unset=True)
        title = updated_fields.get("title", existing["title"])
        description = updated_fields.get("description", existing["description"])
        completed = updated_fields.get("completed", existing["completed"])

        cursor.execute(
            "UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
            (title, description, completed, task_id),
        )
        db.commit()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return dict(row)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_api_key)],
)
def delete_task(task_id: int):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Task not found")
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        db.commit()
        return None
