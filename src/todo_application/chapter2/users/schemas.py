from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from ..tasks.schemas import Task


class UserCreate(BaseModel):
    '''POST /users のリクエストボディが満たすべきスキーマ'''
    name: str

class UserUpdate(BaseModel):
    '''PUT /users/{user_id} のリクエストボディが満たすべきスキーマ'''
    name: str

class User(BaseModel):
    '''レスポンスで返却するユーザー情報が満たすべきスキーマ'''
    user_id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

class UserTasks(User):
    '''GET /users/{user_id}/tasks のレスポンスボディが満たすべきスキーマ'''
    tasks: List[Task]