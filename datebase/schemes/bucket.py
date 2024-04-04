from datetime import datetime
from uuid import UUID
from datebase.models import Bucket

from .base import BaseModelS


class BaseBucketS(BaseModelS):

    def get_model_data(self):
        return super().get_model_data(Bucket)

    class Config:
        from_attributes = True


class CreateBucketS(BaseBucketS):
    user_id: UUID


class GetBucketS(CreateBucketS):
    id_bucket: UUID
    name_bucket: str
    add_at: datetime
