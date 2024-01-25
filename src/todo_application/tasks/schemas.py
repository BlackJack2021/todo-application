from enum import Enum
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class Status(Enum):
    not_started = 'not_started'
    progress = 'progress'
    done = 'done'

class TaskCreate(BaseModel):
    '''POST /tasks のリクエストボディが満たすべきスキーマ'''
    title: str
    description: Optional[str]
    status: Status
    user_id: UUID

class TaskUpdate(BaseModel):
    '''PUT /tasks のリクエストボディが満たすべきスキーマ'''
    title: str
    description: Optional[str]
    status: Status
    user_id: UUID

class Task(BaseModel):
    '''レスポンスで返すタスク情報のスキーマ'''
    title: str
    description: Optional[str]
    status: Status
    user_id: UUID
    task_id: UUID
    created_at: datetime
    updated_at: datetime
    