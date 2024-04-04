from io import BytesIO

from minio import Minio
from minio.datatypes import Bucket
from minio.helpers import ObjectWriteResult

from cryptography.fernet import Fernet

from typing import BinaryIO, List

from common import settings_minio

import aiohttp
import asyncio

class MinioClient:
    __client_instance: Minio = None

    @classmethod
    async def get_instance(cls) -> Minio:

        if cls.__client_instance is None:
            cls.__client_instance = await cls.create_instance()

        return cls.__client_instance

    @classmethod
    async def create_session(cls):
        return aiohttp.ClientSession()


    @classmethod
    async def create_instance(cls) -> Minio:
        minio_client = Minio(
            endpoint=f"{settings_minio.host}:{settings_minio.port}",
            access_key=settings_minio.access_key,
            secret_key=settings_minio.secret_key,
            secure=False,
        )
        
        return minio_client
        
        

    @classmethod
    async def list_buckets(cls) -> List[Bucket]:
        instance = await cls.get_instance()
        return instance.list_buckets()

    @classmethod
    async def put_object(
        cls,
        bucket_name: str,
        object_name: str,
        data: BinaryIO,
        content_type: str,
    ) -> ObjectWriteResult:
        instance = await cls.get_instance()

        return instance.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=data,
            content_type=content_type,
            length=-1,
            part_size=10 * 1024 * 1024,
        )

    @classmethod
    async def put_object_crypt(
        cls,
        bucket_name: str,
        object_name: str,
        data: BinaryIO,
        content_type: str,
        *,
        token: str,
    ) -> ObjectWriteResult:

        fernet = Fernet(token)
        data = fernet.encrypt(data.read())

        return await cls.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=BytesIO(data),
            content_type=content_type,
        )

    @classmethod
    async def get_object(cls, bucket_name: str, object_name: str) -> BinaryIO:
        instance = await cls.get_instance()
        return instance.get_object(
            bucket_name=bucket_name, object_name=object_name
        )

    @classmethod
    async def get_object_crypt(
        cls, bucket_name: str, object_name: str, *, token: str
    ) -> bytes:
        result_object = await cls.get_object(
            bucket_name=bucket_name, object_name=object_name
        )

        return Fernet(token).decrypt(result_object.read())

    @classmethod
    async def bucket_exists(cls, bucket_name: str) -> bool:
        instance = await cls.get_instance()
        return instance.bucket_exists(bucket_name=bucket_name)

    @classmethod
    async def make_bucket(cls, bucket_name: str):
        """AI is creating summary for make_bucket

        Args:
            bucket_name (str): [
                1. Имена ведер должны быть длиной от 3 (мин) до 63 (макс.) Символов.
                2. Имена ведер могут состоять только из строчных букв, цифр, точек (.) И дефисов (-).
                3. Названия ведер не должны содержать двух соседних периодов или периода, прилегающего к дефису.
                4. Имена ведер не должны быть отформатированы как IP-адрес (например, 192.168.5.4).
                5. Имена ведра не должны начинаться с префикса xn--.
                6. Имена ведер не должны заканчиваться суффиксом -s3alias. Этот суффикс зарезервирован для имен псевдонимов точек доступа.
                7. Имена ведер должны быть уникальными в разделе.
            ]

        Returns:
            [type]: [description]
        """

        instance = await cls.get_instance()
        return instance.make_bucket(bucket_name=bucket_name)
