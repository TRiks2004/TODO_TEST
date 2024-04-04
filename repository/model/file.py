from io import BytesIO
from uuid import UUID

from fastapi import UploadFile

from datebase.schemes.bucket import CreateBucketS
from repository.access_levels import AccessLevels, check_access_level
from repository.model.user import RepositoryUserServices
from routs.prefix import TokenSchema
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
                name_file=await get_path_file(
                    str(file_save.id_file), file.name_file
                ),
                data=file.data,
                content_type=file.content_type,
            )
        )

        return file_save


class RepositoryFileBucketServices(RepositoryModelServices[None]):

    def __init__(self):
        super().__init__()

    @classmethod
    async def service_download_file(
        cls, name: str | None, upload_file: UploadFile, token: TokenSchema
    ):
        await check_access_level(token, AccessLevels.defult)
        
        user = await RepositoryUserServices.service_select_user_by_token(token)
        
        bucket_create = CreateBucketS(user_id=user.id_user)
        
        bucket = await RepositoryBucketServices.service_create_bucket_exists(
            bucket=bucket_create
        )

        if name is None:
            name = upload_file.filename
        else:
            name = await get_path_file(name, upload_file.filename)

        file_minio = CreateFileMinioS(
            bucket=bucket.id_bucket,
            name_file=name,
            data=await upload_file.read(),
            content_type=upload_file.content_type,
        )

        fail_save = await RepositoryFileServices.service_save_file(file_minio)
    
        return fail_save


