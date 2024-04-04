from io import BytesIO
from fastapi import Depends, APIRouter, UploadFile, File

from typing import Annotated, List

from repository import RepositoryRoleServices, Role, RepositoryUserServices
from repository.access_levels import AccessLevels, check_access_level

from .prefix import TokenSchema, prefix

from tools.test import MinioClient


file_router = APIRouter(
    prefix=f"/{prefix.file}",
    tags=["FileWork"],
)

from datebase.schemes.bucket import CreateBucketS


@file_router.post("/upload_file")
async def upload_file(
    name: str | None = None,
    upload_file: UploadFile = File(...),
    token: TokenSchema = None,
):

    await check_access_level(token, AccessLevels.defult)
    user = await RepositoryUserServices.service_select_user_by_token(token)

    bucket = CreateBucketS(
        user_id=user.id_user, name_bucket=str(user.id_user) + "-bucket"
    )

    data = upload_file.file.read()

    file_name = (
        upload_file.filename
        if (name is None)
        else name + "." + upload_file.filename.split(".", 1)[1]
    )

    if not await MinioClient.bucket_exists(bucket.name_bucket):
        await MinioClient.make_bucket(bucket.name_bucket)

    # await MinioClient.put_object_crypt(
    #     bucket_name=bucket.name_bucket,
    #     object_name=file_name,
    #     data=BytesIO(data),
    #     content_type=upload_file.content_type,
    #     token="if5nf24JMcKbwUSN2uBvp51AMthSag0kplINubigdKQ=".encode("utf-8")
    # )

    return {"upload_file": upload_file, "token": token}
