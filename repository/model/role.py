from ..RepositoryModel import RepositoryModel, async_session_decorator
from ..RepositoryModelServices import RepositoryModelServices

from datebase.models import Role

from datebase.schemes.role import CreateRoleS

from typing import List

RMRole = Role
"""Repository Model Role - тип данных репозитория ролей"""


class RepositoryRole(RepositoryModel[Role]):

    def __init__(self):
        super().__init__()

    @classmethod
    async def get_by_id(cls, id_role: int) -> Role:
        return await cls.get(cls._MDB.id_role == id_role)

    @classmethod
    async def delete_by_id(cls, id_role: int) -> Role:
        return await cls.delete(cls._MDB.id_role == id_role)

    @classmethod
    async def update_by_id(cls, id_role: int, lavel: int) -> Role:
        return await cls.update(cls.MDB.id_role == id_role, {"lavel": lavel})


class RepositoryRoleServices(RepositoryModelServices[RepositoryRole]):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    async def service_select_all(
        cls, skip: int = 0, limit: int = 100
    ) -> List[Role]:
        return await cls._RMD.get_all(skip, limit)

    @classmethod
    async def service_select_by_id(cls, id_role: int) -> Role:
        return await cls._RMD.get_by_id(id_role)

    @classmethod
    async def service_create(cls, role: CreateRoleS) -> Role:
        return await cls._RMD.add(role.get_model_data())

    @classmethod
    async def service_delete(cls, id_role: int) -> Role:
        return await cls._RMD.delete_by_id(id_role)

    @classmethod
    async def service_update(cls, id_role: int, lavel: int) -> Role:
        return await cls._RMD.update_by_id(id_role, lavel)
