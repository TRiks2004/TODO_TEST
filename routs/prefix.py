from pydantic_settings import BaseSettings

from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader

from typing import TypeAlias, Annotated


class Prefix(BaseSettings):
    identification: str = "identification"
    user: str = "user"
    role: str = "role"


prefix = Prefix()

apikey_scheme = APIKeyHeader(name="Authorization", auto_error=False)

TokenSchema: TypeAlias = Annotated[str, Depends(apikey_scheme)]
