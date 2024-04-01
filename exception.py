from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException

# Информационные ответы (100 – 199)
# Успешные ответы (200 – 299)
# Сообщения о перенаправлении (300 – 399)
# Ошибки клиента (400 – 499)
# Ошибки сервера (500 – 599)

from dataclasses import dataclass
from enum import Enum

import json

class StatusException(Enum):
    authentication: str = "authentication error"

class CodeException(Enum):
    authentication: int = -9809

@dataclass
class DetailException:
    status: StatusException
    code: CodeException
    massage: str    


class BaseHTTPException(HTTPException):
    def __init__(
        self, detail: DetailException = None
    ) -> None:
        self.context = detail
        
        super().__init__(401, self.detail_dict(), None)
        
    def detail_dict(self) -> Dict[str, Any]:
        return {
            'status': self.context.status.value,
            'code': self.context.code.value,
            'massage': self.context.massage
        }
    
    def detail( self,
        status: StatusException, code: CodeException, massage: str
    ):
        return DetailException(status, code, massage)

    
class AuthenticationHttpException(BaseHTTPException):
    
    def __init__(self, massage: str) -> None:
        detail = self.detail(
            StatusException.authentication, CodeException.authentication, massage
        )
        super().__init__(detail)



