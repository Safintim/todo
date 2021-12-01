from fastapi import status
from freezegun import freeze_time

from tests.constants import CURRENT_TIME, DATETIME_RESPONSE
from tests.factories import TaskFactory
from todo.api.router import task_router as router


def test_get_all_tasks(client, create_task) -> None:
    url = router.url_path_for('get_tasks')

    response1 = client.get(url)
    assert response1.status_code == status.HTTP_200_OK
    assert response1.json() == []

    task1 = create_task(title='Task 1')
    task2 = create_task(title='Task 2')

    response2 = client.get(url)

    assert response2.status_code == status.HTTP_200_OK
    assert response2.json() == [
        {'id': task1.id, 'title': 'Task 1'},
        {'id': task2.id, 'title': 'Task 2'},
    ]


@freeze_time(CURRENT_TIME)
def test_get_task(client, create_task) -> None:
    task_attributes = {
        'title': 'New Task',
        'description': 'Description'
    }
    task = create_task(**task_attributes)

    url = router.url_path_for('get_task', task_id=task.id)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': task.id,
        'list_id': task.list_id,
        **DATETIME_RESPONSE,
        **task_attributes,
    }


def test_get_task_not_found(client) -> None:
    not_exists_id = 1

    url = router.url_path_for('get_task', task_id=not_exists_id)
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@freeze_time(CURRENT_TIME)
def test_create_task(client, task_service, create_task_list) -> None:
    task_list = create_task_list()
    task_attributes = TaskFactory.build(list_id=task_list.id)

    url = router.url_path_for('create_task')
    response = client.post(url, json=task_attributes)
    task = task_service.first()
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'id': task.id,
        **DATETIME_RESPONSE,
        **task_attributes,
    }


def test_create_task_validation_error(client) -> None:
    task_attributes = {}

    url = router.url_path_for('create_task')
    response = client.post(url, json=task_attributes)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@freeze_time(CURRENT_TIME)
def test_update_task(client, create_task) -> None:
    task = create_task(title='Old title')
    updated_attributes = TaskFactory.build(list_id=task.list_id, description=task.description)

    url = router.url_path_for('update_task', task_id=task.id)
    response = client.put(url, json=updated_attributes)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': task.id,
        **DATETIME_RESPONSE,
        **updated_attributes,
    }


def test_update_task_validation_error(client, create_task) -> None:
    task = create_task(title='Old title')
    updated_attributes = {'title': 'New title'}

    url = router.url_path_for('update_task', task_id=task.id)
    response = client.put(url, json=updated_attributes)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_task(client, create_task) -> None:
    task = create_task(title='Title')

    url = router.url_path_for('delete_task', task_id=task.id)
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.text == ''


def test_delete_task_not_found(client, create_task) -> None:
    not_exists_id = 1

    url = router.url_path_for('delete_task', task_id=not_exists_id)
    response = client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
