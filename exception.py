from typing import Any, Dict
from fastapi import HTTPException

# Информационные ответы (100 – 199)
# Успешные ответы (200 – 299)
# Сообщения о перенаправлении (300 – 399)
# Ошибки клиента (400 – 499)
# Ошибки сервера (500 – 599)

from dataclasses import dataclass
from enum import Enum


@dataclass
class ExceptionInfo:
    status: str
    code: int

    def to_dict(self) -> Dict[str, Any]:
        return {"status": self.status, "code": self.code}


class ExceptionInfoBlock(Enum):
    authentication: ExceptionInfo = ExceptionInfo(
        status="authentication error", code=-9000
    )

    role_not_found: ExceptionInfo = ExceptionInfo(
        status="role not found", code=-5000
    )
    
    token_not_found: ExceptionInfo = ExceptionInfo(
        status="no access", code=-4000
    )

    denied_access: ExceptionInfo = ExceptionInfo(
        status="denied access", code=0000
    )
    

@dataclass
class DetailException:
    exception_info: ExceptionInfo
    massage: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "exception_info": self.exception_info.to_dict(),
            "massage": self.massage,
        }


class BaseHTTPException(HTTPException):
    def __init__(self, exception_info: ExceptionInfoBlock, massage: str) -> None:
        
        detail = self.detail(exception_info, massage)
        super().__init__(401, detail.to_dict(), None)

    def detail(self, exception_info: ExceptionInfoBlock, massage: str):
        return DetailException(exception_info.value, massage)

# Работа с аутентификацией
class AuthenticationHttpException(BaseHTTPException):

    def __init__(self, massage: str) -> None:
        super().__init__(ExceptionInfoBlock.authentication, massage)


# Работа с ролями
class NoRoleExistsHttpException(BaseHTTPException):
    def __init__(self, massage: str) -> None:
        super().__init__(ExceptionInfoBlock.role_not_found, massage)


# Работа с токенами
class TokenNotFoundHttpException(BaseHTTPException): 
    def __init__(self, massage: str) -> None:
        super().__init__(ExceptionInfoBlock.token_not_found, massage)
        
# Работа с доступом
class DeniedAccessException(BaseHTTPException):
    def __init__(self, massage: str) -> None:
        super().__init__(ExceptionInfoBlock.denied_access, massage)