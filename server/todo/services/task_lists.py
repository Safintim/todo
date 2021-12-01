from todo import models
from todo.services.base import BaseService


class TaskListService(BaseService):
    model = models.TaskListModel
