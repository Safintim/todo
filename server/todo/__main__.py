import uvicorn

from todo.settings import settings

uvicorn.run(
    'todo.app:app',
    host=settings.server_host,
    port=settings.server_port,
    reload=True,
)
