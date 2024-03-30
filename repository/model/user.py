from ..RepositoryModel import RepositoryModel, async_session_decorator
from ..RepositoryModelServices import RepositoryModelServices
from datebase.models import User

from sqlalchemy.ext.asyncio import AsyncSession

class RepositoryUser(RepositoryModel[User]):
    _MDB: User = User

    def __init__(self):
        super().__init__()

    # @classmethod
    # async def get_by_id(cls, id_role: int) -> User:
    #     return await cls.get(cls.MDB.id_role == id_role)

    @classmethod
    async def get_by_login(cls, login: str):
        return await cls.get(cls._MDB.login == login)

    @classmethod
    async def get_hash_password_by_login(cls, login: str):
        return await cls.get_column(
            cls._MDB.login == login, cls._MDB.hash_password
        )

    @classmethod
    @async_session_decorator
    async def get_lavel_by_login(
        cls, login: str, *, session: AsyncSession = None
    ):
        
        return await cls.get_column(cls._MDB.login == login, cls._MDB.id_role)
    
class RepositoryUserServices(RepositoryModelServices):
    
    def __init__(self) -> None:
        super().__init__()

    