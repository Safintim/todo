from todo import models
from todo.services.base import BaseService


class TaskService(BaseService):
    model = models.TaskModel
