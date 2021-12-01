from pydantic import BaseModel, constr


class TaskListScheme(BaseModel):
    """Get all Task Lists"""

    id: int
    title: constr(max_length=150)

    class Config:
        orm_mode = True


class TaskListCreateScheme(BaseModel):
    """Create Task List"""

    title: constr(max_length=150)


class TaskListUpdateScheme(TaskListCreateScheme):
    """Update Task List"""


