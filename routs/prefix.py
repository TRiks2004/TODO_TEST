from pydantic_settings import BaseSettings

from fastapi import Depends
from fastapi.security import APIKeyHeader

from typing import TypeAlias, Annotated


class Prefix(BaseSettings):
    identification: str = "identification"
    user: str = "user"
    role: str = "role"
    file: str = "file"


prefix = Prefix()

apikey_scheme = APIKeyHeader(name="Authorization", auto_error=False)

TokenSchema: TypeAlias = Annotated[str, Depends(apikey_scheme)]
