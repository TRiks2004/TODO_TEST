from datetime import datetime
from typing import BinaryIO
from uuid import UUID
from datebase.models import File

from .base import BaseModelS


class BaseFiletS(BaseModelS):

    def get_model_data(self):
        return super().get_model_data(File)

    class Config:
        from_attributes = True


class CreateFileS(BaseFiletS):
    bucket: UUID
    name_file: str


class GetFileS(CreateFileS):
    id_file: UUID
    add_at: datetime



class CreateFileMinioS(CreateFileS):
    data: bytes
    content_type: str
