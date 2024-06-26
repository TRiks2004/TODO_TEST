from ..RepositoryModelServices import RepositoryModelServices
from .token import RepositoryTokenServices, Token
from .user import RepositoryUserServices

from datebase.schemes.token import SGetToken, SCreateToken

from security import Password, create_token

from exception import AuthenticationHttpException


class RepositoryAuthenticationServices(RepositoryModelServices[None]):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    async def service_authentication(cls, login: str, password: str) -> Token:
        user = await RepositoryUserServices.service_select_by_login(login)

        if user is None:
            raise AuthenticationHttpException("Incorrect login or password")

        verify = await Password.verify(user.hash_password, password)

        if verify:
            auth_token = await create_token()
            token_create = SCreateToken(
                user_id=user.id_user, auth_token=auth_token
            )
            return await RepositoryTokenServices.get_tokens(token_create)
        else:
            raise AuthenticationHttpException("Incorrect login or password")
