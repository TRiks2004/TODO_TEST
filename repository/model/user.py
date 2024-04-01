from ..RepositoryModel import RepositoryModel, async_session_decorator, select
from ..RepositoryModelServices import RepositoryModelServices
from datebase.models import User, Role

from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from typing import List


class RepositoryUser(RepositoryModel[User]):
    _MDB = User
    
    def __init__(self):
        super().__init__()

    @classmethod
    async def get_by_login(cls, login: str):
        return await cls.get(cls._MDB.login == login)

    @classmethod
    async def get_by_id(cls, id_user: UUID):
        return await cls.get(cls._MDB.id_user == id_user)

    @classmethod
    async def get_hash_password_by_login(cls, login: str):
        return await cls.get_column(
            cls._MDB.login == login, cls._MDB.hash_password
        )

    @classmethod
    @async_session_decorator
    async def get_lavel_by_id(
        cls, id_user: UUID, *, session: AsyncSession = None
    ) -> int | None:

        stmt = select(Role.lavel).join(User).where(cls._MDB.id_user == id_user)
        # Выполнение запроса
        result = await session.execute(stmt)
        # Возвращение результата
        return result.scalars().one_or_none()


class RepositoryUserServices(RepositoryModelServices[RepositoryUser]):
    _RMD = RepositoryUser
    
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    async def service_select_all(
        cls, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return await cls._RMD.get_all(skip, limit)

    @classmethod
    async def service_select_by_id(cls, id_user: UUID) -> User:
        return await cls._RMD.get_by_id(id_user)

    @classmethod
    async def service_select_by_login(cls, login: str):
        return await cls._RMD.get_by_login(login)

    @classmethod
    async def service_select_hash_password_by_login(cls, login: str):
        return await cls._RMD.get_hash_password_by_login(login)

    @classmethod
    async def service_select_lavel_by_id(cls, id_user: UUID):
        return await cls._RMD.get_lavel_by_id(id_user)
