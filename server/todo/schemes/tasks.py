from typing import Optional

from pydantic import BaseModel, constr

from todo.schemes.base import Base


class TaskScheme(Base):
    """Get task"""

    description: Optional[str]
    list_id: int

    class Config:
        orm_mode = True


class TaskAllScheme(BaseModel):
    """Get all tasks"""

    id: int
    title: str

    class Config:
        orm_mode = True


class TaskUpdateScheme(BaseModel):
    """Update task"""

    title: constr(max_length=150)
    description: Optional[str]
    list_id: int


class TaskCreateScheme(TaskUpdateScheme):
    """Create task"""
