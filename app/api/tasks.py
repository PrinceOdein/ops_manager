from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskOut
from app.models.task import Task
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskOut)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    new_task = Task(
        title=task.title,
        description=task.description,
        assigned_to=task.assigned_to,
        created_by=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/", response_model=list[TaskOut])
def list_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    limit: int = 20,
    offset: int = 0
):
    query = db.query(Task)

    if current_user.role != "admin":
        query = query.filter(Task.assigned_to == current_user.id)

    return query.limit(limit).offset(offset).all()
