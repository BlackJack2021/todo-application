from datetime import datetime
from typing import List, Literal, Optional, TypedDict
from uuid import UUID
import uuid
from ..tasks.schemas import Status as TaskStatus

class User(TypedDict):
    user_id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

user1_id = uuid.uuid4()
user2_id = uuid.uuid4()

task1_id = uuid.uuid4()
task2_id = uuid.uuid4()

# サンプルのユーザーデータ
users: List[User] = [
    {
        "user_id": user1_id, 
        "name": "ねっと", 
        "created_at": datetime(year=2023, month=1, day=2), 
        "updated_at": datetime(year=2023, month=1, day=4)
    },
    {
        "user_id": user2_id, 
        "name": "さいと", 
        "created_at": datetime(year=2023, month=2, day=2), 
        "updated_at": datetime(year=2023, month=2, day=5)
    },
]

class Task(TypedDict):
    task_id: UUID
    title: str
    description: Optional[str]
    status: TaskStatus
    user_id: UUID
    created_at: datetime
    updated_at: datetime

# サンプルのタスクデータ
tasks: List[Task] = [
    {
        "task_id": task1_id, 
        "title": "宿題", 
        "description": "漢字のノートを書く", 
        "status": TaskStatus.NOT_STARTED,
        "user_id": user1_id, 
        "created_at": datetime(year=2023, month=1, day=2), 
        "updated_at": datetime(year=2023, month=1, day=4)
    },
    {
        "task_id": task2_id, 
        "title": "買い物", 
        "description": "りんごを2つ買う", 
        "status": TaskStatus.PROGRESS, 
        "user_id": user2_id, 
        "created_at": datetime(year=2023, month=2, day=4), 
        "updated_at": datetime(year=2023, month=2, day=8)
    },
]
