from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    assigned_to: Optional[int] = None

class TaskOut(TaskBase):
    id: int
    status: str
    assigned_to: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
