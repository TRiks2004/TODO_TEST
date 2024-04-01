from fastapi import APIRouter, Depends

from typing import Annotated, List

from .prefix import prefix

from datebase.schemes.role import GetRoleS, CreateRoleS

from repository import RepositoryRoleServices as RoleServices, Role

role_router = APIRouter(
    prefix=f'/{prefix.role}',
    tags=['Role'],
)


@role_router.get('/', response_model=List[GetRoleS])
async def get_role_request(skip: int = 0, limit: int = 100) -> List[Role]:
    get = await RoleServices.service_select_all(skip, limit)
    return get


@role_router.get('/{id_role}', response_model=GetRoleS)
async def get_role_by_id_request(id_role: int) -> Role:
    get = await RoleServices.service_select_by_id(id_role)
    return get


@role_router.post('/create', response_model=GetRoleS)
async def create_role_request(role: Annotated[CreateRoleS, Depends()]) -> Role:
    return await RoleServices.service_create(role)


@role_router.post('/delete', response_model=GetRoleS)
async def delete_role_request(
    id_role: int,
) -> Role:
    return await RoleServices.service_delete(id_role)


@role_router.post('/update_lavel', response_model=GetRoleS)
async def update_role_request(id_role: int, lavel: int) -> Role:
    return await RoleServices.service_update(id_role, lavel)
