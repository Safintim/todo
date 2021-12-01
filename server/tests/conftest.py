from typing import Callable, Optional, Any

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.testclient import TestClient

from todo.app import app
from todo.database import get_session
from todo.models import Base, TaskModel, TaskListModel
from todo.services import TaskService, TaskListService
from todo.schemes import TaskCreateScheme, TaskListCreateScheme
from tests.factories import TaskFactory, TaskListFactory
from todo.settings import create_database_url

SQLALCHEMY_DATABASE_URL = create_database_url(database_name='test')


@pytest.fixture(scope='session')
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine
    drop_database(engine.url)


@pytest.fixture(scope='function')
def session(db_engine):
    connection = db_engine.connect()

    connection.begin()
    session = Session(bind=connection)

    yield session

    session.rollback()
    connection.close()


@pytest.fixture(scope='function')
def client(session):
    app.dependency_overrides[get_session] = lambda: session

    with TestClient(app) as c:
        yield c


@pytest.fixture(scope='function')
def task_list_service(session) -> TaskListService:
    return TaskListService(session)


@pytest.fixture(scope='function')
def task_service(session) -> TaskService:
    return TaskService(session)


@pytest.fixture(scope='function')
def create_task_list(task_list_service) -> Callable:
    def inner(**task_list_data: dict) -> TaskListModel:
        task_list_attributes = TaskListFactory.build(**task_list_data)
        return task_list_service.create(TaskListCreateScheme(**task_list_attributes))
    return inner


@pytest.fixture(scope='function')
def create_task(task_service: TaskService, create_task_list: Callable) -> Callable:
    def inner(task_list=None, **task_data: dict) -> TaskModel:
        if task_list is None:
            task_list = create_task_list()

        task_attributes = TaskFactory.build(list_id=task_list.id, **task_data)
        task = task_service.create(TaskCreateScheme(**task_attributes))
        return task
    return inner
