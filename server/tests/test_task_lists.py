from fastapi import status

from tests.factories import TaskListFactory
from todo.api.router import task_lists_router as router


def test_get_all_task_lists(client, create_task_list) -> None:
    url = router.url_path_for('get_task_lists')

    response1 = client.get(url)
    assert response1.status_code == status.HTTP_200_OK
    assert response1.json() == []

    list1 = create_task_list(title='List 1')
    list2 = create_task_list(title='List 2')

    response2 = client.get(url)

    assert response2.status_code == status.HTTP_200_OK
    assert response2.json() == [
        {'id': list1.id, 'title': 'List 1'},
        {'id': list2.id, 'title': 'List 2'},
    ]


def test_create_task_list(client, task_list_service, create_task_list) -> None:
    task_list_attributes = TaskListFactory.build(title='List 1')

    url = router.url_path_for('create_task_list')
    response = client.post(url, json=task_list_attributes)
    task_list = task_list_service.first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'id': task_list.id,
        **task_list_attributes,
    }


def test_create_task_list_validation_error(client) -> None:
    url = router.url_path_for('create_task_list')
    response = client.post(url, json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_task_list(client, create_task_list) -> None:
    task_list = create_task_list(title='Old title')
    updated_attributes = TaskListFactory.build()

    url = router.url_path_for('update_task_list', list_id=task_list.id)
    response = client.put(url, json=updated_attributes)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': task_list.id,
        **updated_attributes,
    }


def test_update_task_list_validation_error(client) -> None:
    url = router.url_path_for('update_task_list', list_id=1)
    response = client.put(url, json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_task(client, create_task_list) -> None:
    task_list = create_task_list(title='Title')

    url = router.url_path_for('delete_task_list', list_id=task_list.id)
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.text == ''
