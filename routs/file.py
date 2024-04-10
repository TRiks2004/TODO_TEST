from fastapi import APIRouter, UploadFile, File

from repository import (
    RepositoryUserServices,
    RepositoryFileServices,
    RepositoryBucketServices,
    RepositoryFileBucketServices
)
from repository.access_levels import AccessLevels, check_access_level

from .prefix import TokenSchema, prefix

from datebase.schemes.bucket import CreateBucketS
from datebase.schemes.file import CreateFileMinioS, GetFileS

from tools.path_file import get_path_file

file_router = APIRouter(
    prefix=f"/{prefix.file}",
    tags=["FileWork"],
)


@file_router.post("/upload_file", response_model=GetFileS)
async def upload_file(
    name: str | None = None,
    upload_file: UploadFile = File(...),
    token: TokenSchema = None,
):
    print()
    
    return await RepositoryFileBucketServices.service_download_file(
        name, upload_file, token
    )
    
