from typing import List

from repository import RepositoryRole, Role

from datebase.schemes.role import CreateRoleS

from .services import Services


class RoleServices(Services):

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    async def service_select_all(
        cls, skip: int = 0, limit: int = 100
    ) -> List[Role]:
        return await RepositoryRole.get_all(skip, limit)

    @classmethod
    async def service_select_by_id(cls, id_role: int) -> Role:
        return await RepositoryRole.get_by_id(id_role)

    @classmethod
    async def service_create(cls, role: CreateRoleS) -> Role:
        return await RepositoryRole.add(role.get_model_data())

    @classmethod
    async def service_delete(cls, id_role: int) -> Role:
        return await RepositoryRole.delete_by_id(id_role)

    @classmethod
    async def service_update(cls, id_role: int, lavel: int) -> Role:
        return await RepositoryRole.update_by_id(id_role, lavel)
