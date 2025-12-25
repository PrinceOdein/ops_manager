from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.models.task import Task
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.audit import AuditLog

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskOut)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if task.assigned_to:
        assignee = db.query(User).filter(User.id == task.assigned_to).first()
    if not assignee:
        raise HTTPException(status_code=404, detail="Assigned user not found")

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
    log = AuditLog(
        user_id=current_user.id,
        action=f"Created task {new_task.id} assigned to user {new_task.assigned_to}"
    )
    db.add(log)
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

@router.patch("/{task_id}/status", response_model=TaskOut)
def update_task_status(
    task_id: int,
    update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if update.status not in ["pending", "active", "done"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    task.status = update.status
    log = AuditLog(
        user_id=current_user.id,
        action=f"Updated task {task.id} status to {task.status}"
    )
    db.add(log)
    db.commit()
    db.refresh(task)
    return task