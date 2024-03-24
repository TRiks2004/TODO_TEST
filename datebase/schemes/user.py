from pydantic import BaseModel, EmailStr

from uuid import UUID

from .role import GetRole

from datetime import datetime


class BaseUser(BaseModel):

    class Config:
        from_attributes = True


class CreateUser(BaseUser):
    id_user: UUID

    login: str
    hash_password: str
    mail: EmailStr
    name: str
    surname: str
    user_role: int
    date_registration: datetime


class GetUser(BaseUser):
    id_user: UUID
    login: str
    hash_password: str
    mail: EmailStr
    name: str
    surname: str
    user_role: int
    date_registration: datetime
