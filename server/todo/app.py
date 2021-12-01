from fastapi import FastAPI

from todo.api import router


app = FastAPI()

app.include_router(router)


@app.get('/')
def hello():
    return {'message': 'Hello'}
