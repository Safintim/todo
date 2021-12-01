from datetime import datetime

from pydantic import BaseModel, constr


class Base(BaseModel):
    id: int
    title: constr(max_length=150)
    created_at: datetime
    updated_at: datetime
