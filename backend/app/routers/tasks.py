from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import Project, Task
from ..schemas import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

def serialize(task: Task):
    data = TaskOut.model_validate(task).model_dump()
    data["project_name"] = task.project.name if task.project else None
    return data

@router.get("", response_model=list[TaskOut])
def list_tasks(status_filter: str | None = Query(default=None, alias="status"), project_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Task).options(joinedload(Task.project))
    if status_filter:
        query = query.filter(Task.status == status_filter)
    if project_id is not None:
        query = query.filter(Task.project_id == project_id)
    return [serialize(task) for task in query.order_by(Task.created_at.desc()).all()]

@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    if payload.project_id is not None and db.get(Project, payload.project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")
    task = Task(**payload.model_dump(), completed=payload.status == "done")
    db.add(task)
    db.commit()
    db.refresh(task)
    return serialize(task)

@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).options(joinedload(Task.project)).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    changes = payload.model_dump(exclude_unset=True)
    if changes.get("project_id") is not None and db.get(Project, changes["project_id"]) is None:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in changes.items():
        setattr(task, key, value)
    if "status" in changes:
        task.completed = changes["status"] == "done"
    db.commit()
    db.refresh(task)
    return serialize(task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
