import datetime
from uuid import UUID
from ..RepositoryModel import (
    RepositoryModel,
    async_session_decorator,
    select,
    AsyncSession,
)
from ..RepositoryModelServices import RepositoryModelServices

from datebase.models import Token

from datebase.schemes.token import SCreateToken, SGetToken

from typing import List


class RepositoryToken(RepositoryModel[Token]):

    def __init__(self):
        super().__init__()

    @classmethod
    @async_session_decorator
    async def get_tokens(
        cls, user_id: UUID, *, session: AsyncSession = None
    ) -> Token | None:
        stmt = (
            select(cls._MDB)
            .where(cls._MDB.user_id == user_id)
            .order_by(cls._MDB.create_at)
            .limit(1)
        )
        result = await session.execute(stmt)

        return result.scalars().one_or_none()

    @classmethod
    async def create_token(cls, create_token: SCreateToken) -> Token | None:
        return await cls.add(create_token.get_model_data())

    @classmethod
    async def delete_token(cls, token_id: UUID) -> Token | None:
        return await cls.delete(cls._MDB.id_token == token_id)


class RepositoryTokenServices(RepositoryModelServices[RepositoryToken]):

    def __init__(self):
        super().__init__()

    @classmethod
    async def get_tokens(cls, create_token: SCreateToken):
        token = await cls._RMD.get_tokens(create_token.user_id)

        if token:
            end_life_cycle_token = token.create_at + token.life_cycle

            if end_life_cycle_token < datetime.datetime.now(tz=datetime.UTC):
                delete_token = await RepositoryToken.delete_token(
                    token.id_token
                )
                return await cls._RMD.create_token(create_token)
            return token
        else:
            return await cls._RMD.create_token(create_token)
