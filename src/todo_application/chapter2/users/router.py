from fastapi import APIRouter, HTTPException
from typing import Optional, List
from starlette import status

from .schemas import User, UserCreate, UserUpdate
from ..db_mock.db import users
import uuid
from uuid import UUID
from datetime import datetime

router = APIRouter()

def user_not_found_message(user_id: UUID) -> str:
    '''ユーザーが見つからない場合の例外メッセージの生成'''
    return f'指定されたユーザー user_id={user_id} が存在しません'

@router.get("/users")
async def get_users(
    limit: Optional[int] = None
) -> List[User]:
    '''ユーザーのコレクションを取得する
    
    Args:
        limit (Optional[int]) : ユーザーを最大何人まで取得するかを指定。Noneならすべてを取得
        
    Returns:
        List[Task] : ユーザーのコレクション
    '''

    if limit is not None and len(users) > limit:
        return users[:limit]
    
    return users

@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    request_body: UserCreate
) -> User:
    '''ユーザーを追加する'''
    user_id = uuid.uuid4()
    created_at = datetime.now()
    updated_at = datetime.now()
    new_user: User = {
        'user_id': user_id,
        'name': request_body.name,
        'created_at': created_at,
        'updated_at': updated_at
    }
    users.append(new_user)
    return new_user

@router.get('/users/{user_id}')
async def get_user(
    user_id: UUID
) -> User:
    '''指定されたユーザーを取得する'''
    for user in users:
        if user['user_id'] == user_id:
            return user
    HTTPException(
        status_code=404,
        detail=user_not_found_message(user_id)
    )

@router.put('/users/{user_id}')
async def update_user(
    user_id: UUID,
    request_body: UserUpdate
) -> User:
    '''指定されたユーザーのデータを更新'''
    request_body_dict = request_body.model_dump()
    for user in users:
        if user['user_id'] == user_id:
            user.update(request_body_dict)
            user['updated_at'] = datetime.now()
            return user
    HTTPException(
        status_code=404,
        detail=user_not_found_message(user_id)
    )

@router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID
):
    '''指定されたユーザーを削除する'''
    for index, user in enumerate(users):
        if user['user_id'] == user_id:
            users.pop(index)
            return
    raise HTTPException(
        status_code=404,
        detail=user_not_found_message(user_id)
    )