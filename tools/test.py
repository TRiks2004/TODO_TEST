import os
import sys

import pathlib

sys.path.append(os.getcwd())

from repository import RepositoryBucketServices, RepositoryFileServices
from datebase.schemes.bucket import CreateBucketS
from datebase.schemes.file import CreateFileMinioS
import random

from datebase import MinioClient


async def main():
    """bucket_name = "python-test-bucket"
    object_name = "my-test-file52.py"

    token = "if5nf24JMcKbwUSN2uBvp51AMthSag0kplINubigdKQ=".encode("utf-8")

    with open(
        pathlib.Path(__file__).parent / "create_headers_env.py", "rb"
    ) as f:

        result = await MinioClient.put_object_crypt(
            bucket_name=bucket_name,
            object_name=object_name,
            data=f,
            content_type="application/octet-stream",
            token=token,
        )

        print(result)

    with open(
        pathlib.Path(__file__).parent / "create_headers_env_get.py", "+bw"
    ) as f:

        result = await MinioClient.get_object_crypt(
            bucket_name=bucket_name, object_name=object_name, token=token
        )

        f.write(result)"""

    bucket = await RepositoryBucketServices.service_create_bucket_exists(
        bucket=CreateBucketS(
            user_id="b9d2145e-b150-4e32-b05d-16dcbe6071bb",
        )
    )

    print('\n\n')
    print(await bucket.model_to_dict())
    print('\n\n')
    
    with open(
        pathlib.Path(__file__).parent / "create_headers_env.py", "rb"
    ) as f:
        file_minio = CreateFileMinioS(
            bucket=bucket.id_bucket,
            name_file='test.py',
            data=f.read(),
            content_type="application/octet-stream",
        )

        fail_save = await RepositoryFileServices.service_save_file(file_minio)

        print('\n\n')
        print(await fail_save.model_to_dict())
        print('\n\n')


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
