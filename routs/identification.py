from repository import RepositoryAuthenticationServices

from datebase.schemes.token import SGetToken
from fastapi import Depends, APIRouter

from repository.access_levels import AccessLevels, check_access_level

from .prefix import prefix, TokenSchema

# Аутентификация
# Этот процесс проверки подлинности идентификации пользователя или системы.
# В основном, аутентификация отвечает на вопрос 'Кто вы?'.
# Это может быть выполнено с использованием различных методов,
#   таких как пароли, биометрические данные (отпечатки пальцев, распознавание лица и т.д.),
#   смарт-карты, токены и другие технологии. Цель аутентификации - удостовериться,
#   что пользователь или система являются тем, за кого они себя выдают.


identification_router = APIRouter(
    prefix=f"/{prefix.identification}",
    tags=["Identification"],
)


@identification_router.get("/authe", response_model=SGetToken)
async def authentication(login: str, password: str):
    return await RepositoryAuthenticationServices.service_authentication(
        login, password
    )


# Авторизация
# После успешной аутентификации, авторизация определяет разрешения и права доступа,
#   которые у пользователя или системы есть в системе или приложении.
# Она отвечает на вопрос 'Что вы можете сделать?'.
# Это контролирует, какие ресурсы, данные или функциональность доступны
#   пользователю после успешного входа в систему.
# Например, пользователь может быть аутентифицирован как сотрудник компании,
#   но его доступ к конфиденциальной информации может быть ограничен в соответствии с его ролью или полномочиями.


@identification_router.get("/autho")
async def authorization(token: TokenSchema):
    check = await check_access_level(token, AccessLevels.defult)
    return check
