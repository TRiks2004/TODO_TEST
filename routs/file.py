from io import BytesIO
from fastapi import Depends, APIRouter, UploadFile, File

from typing import Annotated, List

from repository import (
    RepositoryUserServices,
    RepositoryFileServices,
    RepositoryBucketServices,
)
from repository.access_levels import AccessLevels, check_access_level

from .prefix import TokenSchema, prefix

from tools.test import MinioClient

from datebase.schemes.bucket import CreateBucketS
from datebase.schemes.file import CreateFileMinioS

from tools.path_file import get_path_file

file_router = APIRouter(
    prefix=f"/{prefix.file}",
    tags=["FileWork"],
)


@file_router.post("/upload_file")
async def upload_file(
    name: str | None = None,
    upload_file: UploadFile = File(...),
    token: TokenSchema = None,
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

    return {"upload_file": upload_file, "token": token}
