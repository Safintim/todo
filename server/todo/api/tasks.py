from fastapi import APIRouter, Depends, Response, status

from todo.schemes import TaskScheme, TaskAllScheme, TaskCreateScheme, TaskUpdateScheme
from todo.services import TaskService

task_router = APIRouter(prefix='/tasks')

service_depends = Depends(TaskService)


@task_router.get('/', response_model=list[TaskAllScheme])
def get_tasks(service: TaskService = service_depends):
    return service.get_all()


@task_router.get('/{task_id}', response_model=TaskScheme)
def get_task(task_id: int, service: TaskService = service_depends):
    return service.get(task_id)


@task_router.post('/', response_model=TaskScheme, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreateScheme, service: TaskService = service_depends):
    return service.create(task)


@task_router.put('/{task_id}', response_model=TaskScheme)
def update_task(task_id: int, task: TaskUpdateScheme, service: TaskService = service_depends):
    return service.update(task_id, task)


@task_router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, service: TaskService = service_depends) -> Response:
    service.delete(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
