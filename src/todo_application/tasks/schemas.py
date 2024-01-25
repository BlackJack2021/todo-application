from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


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
    