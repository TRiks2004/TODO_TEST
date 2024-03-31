from .base import BaseModelS

from uuid import UUID

from datetime import datetime, timedelta

from datebase.models import Token

class SBaseToken(BaseModelS):

    def get_model_data(self):
        return super().get_model_data(Token)
    
    class Config:
        from_attributes = True

class SCreateToken(SBaseToken):
    auth_token: str
    user_id: UUID
    life_cycle: timedelta | None = None


class SGetToken(SCreateToken):
    id_token: UUID