from fastapi import FastAPI

from .tasks.router import router as task_router
from .users.router import router as user_router

app = FastAPI()

app.include_router(task_router)
app.include_router(user_router)