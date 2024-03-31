import datetime
from uuid import UUID
from ..RepositoryModel import RepositoryModel, async_session_decorator, select, AsyncSession
from ..RepositoryModelServices import RepositoryModelServices

from datebase.models import Token

from datebase.schemes.token import SCreateToken, SGetToken

from typing import List

class RepositoryToken(RepositoryModel[Token]):
    _MDB = Token

    def __init__(self):
        super().__init__()
    
    @classmethod
    @async_session_decorator
    async def get_tokens(cls, user_id: UUID, *, session: AsyncSession = None) -> Token | None:
        stmt = select(cls._MDB).where(cls._MDB.user_id == user_id).order_by(cls._MDB.create_at).limit(1)
        result = await session.execute(stmt)
        
        return result.scalars().one_or_none()

    @classmethod
    @async_session_decorator
    async def create_token(cls, create_token: SCreateToken, *, session: AsyncSession = None) -> Token | None:
        
        token = await cls.get_tokens(user_id=create_token.user_id, session=session)
        
        if token:
            
            end_life_cycle_token = token.create_at + token.life_cycle
            
            if end_life_cycle_token < datetime.datetime.now(tz=datetime.UTC):
                await cls.delete_token(token.id_token)
                return await cls.add(cls._MDB(**create_token.model_dump()), session=session)
            
            return token
        else:
            return await cls.add(cls._MDB(**create_token.model_dump()), session=session)
        
    @classmethod
    async def delete_token(cls, token_id: UUID) -> Token | None:
        return await cls.delete(cls._MDB.id_token == token_id)