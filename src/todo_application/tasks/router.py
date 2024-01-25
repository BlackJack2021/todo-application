from fastapi import APIRouter, HTTPException

from typing import Optional, List
from .schemas import Status, TaskCreate, TaskUpdate, Task
from ..db_mock.db import tasks
import uuid
from uuid import UUID
from datetime import datetime
from starlette import status

router = APIRouter()

def task_not_found_message(task_id: UUID) -> str:
    '''タスクが見つからない場合の例外メッセージの生成'''
    return f'指定されたタスク task_id={task_id} が存在しません'

@router.get("/tasks")
async def get_tasks(
    limit: Optional[int] = None,
    status: Optional[Status] = None
) -> List[Task]:
    '''タスクのコレクションを取得する
    
    Args:
        limit (Optional[int]) : タスクを最大何個まで返すかを指定。Noneなら該当したタスクを全て返す
        status (Optional[Status]) : status を確認し、該当するもののみを抽出
        
    Returns:
        List[Task] : 条件に基づいて抽出されたタスクのリスト
    '''
    _tasks = tasks.copy()
    
    # status に条件があればフィルタリング
    if status is not None:
        _tasks = [_task for _task in _tasks if _task['status'] == status.value]
    
    # limit が指定されていればその数に限定
    if limit is not None:
        _tasks = _tasks[:limit]
    
    return _tasks

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(
    request_body: TaskCreate
) -> Task:
    '''タスクを追加する'''
    task_id = str(uuid.uuid4())
    created_at = datetime.today()
    updated_at = datetime.today()
    new_task = {
        'title': request_body.title,
        'description': request_body.description,
        'status': request_body.status.value,
        'user_id': request_body.user_id,
        'task_id': task_id,
        'created_at': created_at,
        'updated_at': updated_at
    }
    tasks.append(new_task)
    return new_task
    
@router.get('/tasks/{task_id}')
async def get_task(
    task_id: UUID,
) -> Task:
    '''指定されたタスクを取得する'''
    for task in tasks:
        if task['task_id'] == str(task_id):
            return task
    raise HTTPException(
        status_code=404,
        detail=task_not_found_message(task_id)
    )
    
      
@router.put('/tasks/{task_id}')
async def update_task(
    task_id: UUID,
    request_body: TaskUpdate
) -> Task:
    '''指定されたタスクを更新する'''
    request_body_dict = request_body.model_dump()
    for task in tasks:
        if task['task_id'] == str(task_id):
            task.update(request_body_dict)
            task['updated_at'] = datetime.today()
            return task
    raise HTTPException(
        status_code=404,
        detail=task_not_found_message(task_id)
    )

@router.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID
):
    '''指定されたタスクを削除する'''
    for index, task in enumerate(tasks):
        if task['task_id'] == str(task_id):
            tasks.pop(index)
            return
    raise HTTPException(
        status_code=404,
        detail=task_not_found_message(task_id)
    )