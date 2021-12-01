from fastapi import APIRouter, Depends, Response, status

from todo.schemes import TaskListScheme, TaskListUpdateScheme, TaskListCreateScheme
from todo.services import TaskListService

task_lists_router = APIRouter(prefix='/lists')

service_depends = Depends(TaskListService)


@task_lists_router.get('/', response_model=list[TaskListScheme])
def get_task_lists(service: TaskListService = service_depends):
    return service.get_all()


@task_lists_router.post('/', response_model=TaskListScheme, status_code=status.HTTP_201_CREATED)
def create_task_list(task_list: TaskListCreateScheme, service: TaskListService = service_depends):
    return service.create(task_list)


@task_lists_router.put('/{list_id}', response_model=TaskListScheme)
def update_task_list(list_id: int, task_list: TaskListUpdateScheme, service: TaskListService = service_depends):
    return service.update(list_id, task_list)


@task_lists_router.delete('/{list_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task_list(list_id: int, service: TaskListService = service_depends):
    service.delete(list_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


