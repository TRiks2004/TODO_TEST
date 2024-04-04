from ..RepositoryModel import (
    RepositoryModel,
    async_session_decorator,
    AsyncSession,
    select,
)
from ..RepositoryModelServices import RepositoryModelServices

from datebase.models import Role, User, Token

from datebase.schemes.role import CreateRoleS

from typing import List


class RepositoryRole(RepositoryModel[Role]):

    _MDB = Role

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
        return await cls.update(cls._MDB.id_role == id_role, {"lavel": lavel})

    @classmethod
    @async_session_decorator
    async def get_lavel_by_token(
        cls, token: str, *, session: AsyncSession = None
    ) -> int | None:
        stmt = (
            select(cls._MDB.lavel)
            .join(User, User.user_role == cls._MDB.id_role)
            .join(Token, Token.user_id == User.id_user)
            .where(Token.auth_token == token)
        )

        result = await session.execute(stmt)

        return result.scalars().one_or_none()


class RepositoryRoleServices(RepositoryModelServices[RepositoryRole]):
    _RMD = RepositoryRole

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

    @classmethod
    async def get_lavel_by_token(cls, token: str) -> int | None:
        return await cls._RMD.get_lavel_by_token(token)
