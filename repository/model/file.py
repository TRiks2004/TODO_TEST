from io import BytesIO
from uuid import UUID
from ..RepositoryModel import (
    RepositoryModel,
    async_session_decorator,
    AsyncSession,
    select,
)
from ..RepositoryModelServices import RepositoryModelServices

from datebase.models import Bucket, File

from datebase.schemes.file import CreateFileS, GetFileS, CreateFileMinioS

from typing import List

from datebase import MinioClient

from .bucket import RepositoryBucketServices
from tools.path_file import get_path_file


class RepositoryFile(RepositoryModel[File]):
    _MDB = File

    def __init__(self):
        super().__init__()

    @classmethod
    async def create_file(cls, file: CreateFileS) -> File:
        return await cls.add(file.get_model_data())


class RepositoryFileServices(RepositoryModelServices[RepositoryFile]):
    _RMD = RepositoryFile

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    async def _service_create_file_postgres(cls, file: CreateFileS):
        return await cls._RMD.create_file(file)

    @classmethod
    async def _service_create_file_minio(cls, file: CreateFileMinioS):
        backet = await RepositoryBucketServices.service_select_by_id(
            file.bucket
        )

        await MinioClient.put_object(
            backet.name_bucket,
            file.name_file,
            BytesIO(file.data),
            file.content_type,
        )

    @classmethod
    async def service_save_file(cls, file: CreateFileMinioS):
        file_save = await cls._service_create_file_postgres(
            CreateFileS(bucket=file.bucket, name_file=file.name_file)
        )

        await cls._service_create_file_minio(
            CreateFileMinioS(
                bucket=file.bucket,
                name_file=get_path_file(
                    str(file_save.id_file), file.name_file
                ),
                data=file.data,
                content_type=file.content_type,
            )
        )

        return file_save
