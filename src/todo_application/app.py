from fastapi import FastAPI

from .tasks.router import router as task_router

app = FastAPI()

@app.get('/hello')
def say_hello():
    return {
        'hello': 'world!'
    }

app.include_router(task_router)