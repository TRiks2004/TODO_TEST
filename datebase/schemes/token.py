from pydantic import BaseModel

from uuid import UUID

from datetime import datetime, timedelta

class SBaseToken(BaseModel):

    class Config:
        from_attributes = True

class SCreateToken(SBaseToken):
    auth_token: str
    user_id: UUID
    life_cycle: timedelta | None = None


class SGetToken(SCreateToken):
    id_token: UUID