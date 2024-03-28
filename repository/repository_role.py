from .repository import Repository
from datebase.models import Role

RMRole = Role
"""Repository Model Role - тип данных репозитория ролей"""


class RepositoryRole(Repository[Role]):
    MDB: Role = Role

    def __init__(self):
        super().__init__()

    @classmethod
    async def get_by_id(cls, id_role: int) -> Role:
        return await cls.get(cls.MDB.id_role == id_role)

    @classmethod
    async def delete_by_id(cls, id_role: int) -> Role:
        return await cls.delete(cls.MDB.id_role == id_role)

    @classmethod
    async def update_by_id(cls, id_role: int, lavel: int) -> Role:
        return await cls.update(cls.MDB.id_role == id_role, {"lavel": lavel})
