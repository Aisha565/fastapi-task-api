from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import TaskRow, UserRow, get_db
from schemas import TaskCreate, Task, TaskUpdate
from routers.auth import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


# -------------------------
# GET all tasks
# -------------------------

@router.get("")
def list_tasks(
    limit: int = 10,
    done: bool = False,
    db: Session = Depends(get_db)
    # current_user: UserRow = Depends(get_current_user)
):
    results = (
        db.query(TaskRow)
        .filter(
            TaskRow.done == done
            # TaskRow.user_id == current_user.id
        )
        .limit(limit)
        .all()
    )

    return {
        "limit": limit,
        "done": done,
        "tasks": results
    }

# -------------------------
# GET single task
# -------------------------

@router.get("/{task_id}")
def get_task(
    task_id: int,
    include_details: bool = False,
    db: Session = Depends(get_db),
    current_user: UserRow = Depends(get_current_user)
):
    
    task = (
        db.query(TaskRow)
        .filter(
            TaskRow.id == task_id,
            TaskRow.user_id == current_user.id
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "task": task,
        "include_details": include_details
    }


# -------------------------
# POST - Create task
# -------------------------

@router.post("", response_model=Task, status_code=201)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserRow = Depends(get_current_user)
):
    new_task = TaskRow(
        **task_data.model_dump(),
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# -------------------------
# PUT - Update task
# -------------------------

@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserRow = Depends(get_current_user)
):
    task = (
        db.query(TaskRow)
        .filter(
            TaskRow.id == task_id,
            TaskRow.user_id == current_user.id
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = updated_task.title
    task.description = updated_task.description
    task.priority = updated_task.priority
    task.due_date = updated_task.due_date

    db.commit()
    db.refresh(task)

    return task

# -------------------------
# PATCH - Partially update task
# -------------------------

@router.patch("/{task_id}", response_model=Task)
def patch_task(
    task_id: int,
    updated_task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: UserRow = Depends(get_current_user)
):
    task = (
        db.query(TaskRow)
        .filter(
            TaskRow.id == task_id,
            TaskRow.user_id == current_user.id
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = updated_task.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


# -------------------------
# DELETE - Remove task
# -------------------------

@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserRow = Depends(get_current_user)
):
    task = (
        db.query(TaskRow)
        .filter(
            TaskRow.id == task_id,
            TaskRow.user_id == current_user.id
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return