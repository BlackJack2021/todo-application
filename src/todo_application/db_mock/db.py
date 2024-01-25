from datetime import datetime
from typing import List, Literal, Optional, TypedDict
from uuid import UUID


class User(TypedDict):
    user_id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

# サンプルのユーザーデータ
users: List[User] = [
    {
        "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479", 
        "name": "ねっと", 
        "created_at": datetime(year=2023, month=1, day=2), 
        "updated_at": datetime(year=2023, month=1, day=4)
    },
    {
        "user_id": "e83b5f8d-bf1e-4a0d-8b70-97d6eeb6dade", 
        "name": "さいと", 
        "created_at": datetime(year=2023, month=2, day=2), 
        "updated_at": datetime(year=2023, month=2, day=5)
    },
]

class Task(TypedDict):
    task_id: UUID
    title: str
    description: Optional[str]
    status: Literal['not_started', 'progress', 'done']
    user_id: UUID
    created_at: datetime
    updated_at: datetime

# サンプルのタスクデータ
tasks: List[Task] = [
    {
        "task_id": "a1b2c3d4-5678-90ab-cdef-123456abcdef", 
        "title": "宿題", 
        "description": "漢字のノートを書く", 
        "status": "not_started", 
        "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479", 
        "created_at": datetime(year=2023, month=1, day=2), 
        "updated_at": datetime(year=2023, month=1, day=4)
    },
    {
        "task_id": "abcdef12-3456-7890-abcd-ef1234567890", 
        "title": "買い物", 
        "description": "りんごを2つ買う", 
        "status": "progress", 
        "user_id": "e83b5f8d-bf1e-4a0d-8b70-97d6eeb6dade", 
        "created_at": datetime(year=2023, month=2, day=4), 
        "updated_at": datetime(year=2023, month=2, day=8)
    },
]
