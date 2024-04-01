from fastapi import APIRouter, Depends

from typing import Annotated, List

from .prefix import prefix

from datebase.schemes.user import GetUser

from repository import RepositoryUserServices as UserServices, User

from uuid import UUID

user_router = APIRouter(
    prefix=f'/{prefix.user}',
    tags=['User'],
)


@user_router.get('/', response_model=List[GetUser])
async def get_role_request(skip: int = 0, limit: int = 100):
    get = await UserServices.service_select_all(skip, limit)
    return get


@user_router.get('/{id_user}', response_model=GetUser)
async def get_role_by_id_request(id_user: UUID) -> User:
    get = await UserServices.service_select_by_id(id_user)
    return get


@user_router.get('password/{login}', response_model=str)
async def get_hash_password_by_login_request(login: str) -> str:
    return await UserServices.service_select_hash_password_by_login(login)


@user_router.get('/lavel/{id_user}', response_model=int)
async def get_lavel_by_id_request(id_user: UUID) -> int:
    return await UserServices.service_select_lavel_by_id(id_user)
