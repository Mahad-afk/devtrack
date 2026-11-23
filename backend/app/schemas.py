from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

TaskStatus = Literal["todo", "in_progress", "done"]
Priority = Literal["low", "medium", "high"]

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = ""
    color: str = "#7c6cf2"

class ProjectOut(ProjectCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    description: str = ""
    status: TaskStatus = "todo"
    priority: Priority = "medium"
    due_date: str | None = None
    project_id: int | None = None

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = None
    status: TaskStatus | None = None
    priority: Priority | None = None
    due_date: str | None = None
    project_id: int | None = None

class TaskOut(TaskCreate):
    id: int
    completed: bool
    created_at: datetime
    project_name: str | None = None
    model_config = ConfigDict(from_attributes=True)
