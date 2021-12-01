from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class CommonFields:
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(150), nullable=False)
    updated_at = sa.Column(
        sa.DateTime(timezone=True),
        default=lambda: datetime.now(),
        onupdate=lambda: datetime.now(),
    )
    created_at = sa.Column(sa.DateTime(timezone=True), default=lambda: datetime.now())


class TaskListModel(CommonFields, Base):
    __tablename__ = 'todo_tasklist'


class TaskModel(CommonFields, Base):
    __tablename__ = 'todo_task'

    description = sa.Column(sa.Text)
    list_id = sa.Column(sa.Integer, sa.ForeignKey('todo_tasklist.id'))

