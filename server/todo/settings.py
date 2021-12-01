import os
from typing import Optional

from pydantic import BaseSettings


def create_database_url(database_name: Optional[str] = None) -> str:
    user = os.environ.get('DATABASE_USER')
    password = os.environ.get('DATABASE_PASSWORD')
    host = os.environ.get('DATABASE_HOST')
    name = database_name or os.environ.get('DATABASE_NAME')
    return f'postgresql://{user}:{password}@{host}/{name}'


class Settings(BaseSettings):
    server_host: str = '0.0.0.0'
    server_port: int = 8000
    database_url: str = create_database_url()


settings = Settings()
