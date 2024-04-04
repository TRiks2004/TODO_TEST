from uuid import UUID
from ..RepositoryModel import (
    RepositoryModel,
    async_session_decorator,
    AsyncSession,
    select,
)
from ..RepositoryModelServices import RepositoryModelServices

from datebase.models import Role, User, Token, Bucket

from datebase.schemes.bucket import CreateBucketS, GetBucketS

from typing import List

from datebase import MinioClient


class RepositoryBucket(RepositoryModel[Bucket]):

    _MDB = Bucket

    def __init__(self):
        super().__init__()

    @classmethod
    async def create_bucket(cls, bucket: CreateBucketS) -> Bucket:
        return await cls.add(bucket.get_model_data())

    @classmethod
    async def get_by_id(cls, id_bucket: UUID) -> Bucket:
        return await cls.get(cls._MDB.id_bucket == id_bucket)


class RepositoryBucketServices(RepositoryModelServices[RepositoryBucket]):
    
    _RMD = RepositoryBucket

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    async def _service_create_bucket_postgres(
        cls, bucket: CreateBucketS
    ) -> Bucket:
        return await cls._RMD.create_bucket(bucket)

    @classmethod
    async def _service_bucket_exists_postgres(cls, user_id: UUID):
        return await cls._RMD.get(cls._RMD._MDB.user_id == user_id)

    @classmethod
    async def _service_create_bucket_minio(cls, bucket: Bucket):
        await MinioClient.make_bucket(bucket.name_bucket)

    @classmethod
    async def _service_bucket_exists_minio(cls, bucket: Bucket):
        return await MinioClient.bucket_exists(bucket.name_bucket)

    @classmethod
    async def service_create_bucket_exists(
        cls, bucket: CreateBucketS
    ) -> Bucket:
        bucket_exists = await cls._service_bucket_exists_postgres(
            bucket.user_id
        )
        if bucket_exists is not None:
            bucket = bucket_exists
        else:
            bucket = await cls._service_create_bucket_postgres(bucket)

        if not await cls._service_bucket_exists_minio(bucket):
            await cls._service_create_bucket_minio(bucket)

        return bucket

    @classmethod
    async def service_select_by_id(cls, id_bucket: UUID) -> Bucket:
        return await cls._RMD.get_by_id(id_bucket)

# if not await MinioClient.bucket_exists(
#         bucket.name_bucket
#     ):
#         await MinioClient.make_bucket(bucket.name_bucket)
