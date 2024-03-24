from fastapi import APIRouter, Depends

from typing import List
from uuid import UUID

from .prefix import prefix

from datebase.connect import get_async_session

from datebase.schemes.role import GetRole
from datebase.schemes.user import GetUser

from sqlalchemy.ext.asyncio import AsyncSession

from services.user_services import (
    select_all_role, select_role_by_id, select_user, select_user_by_id
)

user_router = APIRouter(
    prefix=f'/{prefix.user}',
    tags=['User'],
)

@user_router.get('/role', response_model=List[GetRole])
async def get_role(
    skip: int = 0, limit: int = 100, 
    session: AsyncSession = Depends(get_async_session)
):
    get = await select_all_role(session, skip, limit)
    return get
    
@user_router.get('/role/{id_role}', response_model=GetRole)
async def get_role_by_id(
    id_role: int,
    session: AsyncSession = Depends(get_async_session)
):
    get = await select_role_by_id(session, id_role)
    return get

@user_router.get('/', response_model=List[GetUser])
async def get_user(
    skip: int = 0, limit: int = 100, 
    session: AsyncSession = Depends(get_async_session)
):
    get = await select_user(session, skip, limit)
    return get

@user_router.get('/{id_user}', response_model=GetUser)
async def get_user_by_id(
    id_user: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    get = await select_user_by_id(session, id_user)
    return get




