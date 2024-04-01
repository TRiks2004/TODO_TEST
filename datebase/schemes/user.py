from pydantic import BaseModel, EmailStr

from uuid import UUID

from datetime import datetime


class BaseUser(BaseModel):

    class Config:
        from_attributes = True


class CreateUser(BaseUser):
    login: str
    hash_password: str
    mail: EmailStr
    name: str
    surname: str
    user_role: int
    date_registration: datetime


class GetUser(CreateUser):
    id_user: UUID
