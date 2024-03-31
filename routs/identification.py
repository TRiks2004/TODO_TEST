from fastapi import APIRouter

from .prefix import prefix


from repository import RepositoryToken, Token

from datebase.schemes.token import SGetToken, SCreateToken

identification_router = APIRouter(
    prefix=f"/{prefix.identification}",
    tags=["Identification"],
)


# Аутентификация
# Этот процесс проверки подлинности идентификации пользователя или системы.
# В основном, аутентификация отвечает на вопрос "Кто вы?".
# Это может быть выполнено с использованием различных методов,
#   таких как пароли, биометрические данные (отпечатки пальцев, распознавание лица и т.д.),
#   смарт-карты, токены и другие технологии. Цель аутентификации - удостовериться,
#   что пользователь или система являются тем, за кого они себя выдают.


from repository import RepositoryUserServices 
from security.password import Password


@identification_router.get("/authe")
async def authentication(login: str, password: str):
    # TODO: Переписать на отдельный сервис
    user = await RepositoryUserServices.service_select_by_login(login)    
    verify = await Password.verify(user.hash_password, password)
    
    if verify:
        return await RepositoryToken.create_token(SCreateToken(user_id=user.id_user, auth_token='test'))
    else:
        return "Authentication failed" 


# Авторизация
# После успешной аутентификации, авторизация определяет разрешения и права доступа,
#   которые у пользователя или системы есть в системе или приложении.
# Она отвечает на вопрос "Что вы можете сделать?".
# Это контролирует, какие ресурсы, данные или функциональность доступны
#   пользователю после успешного входа в систему.
# Например, пользователь может быть аутентифицирован как сотрудник компании,
#   но его доступ к конфиденциальной информации может быть ограничен в соответствии с его ролью или полномочиями.


@identification_router.get("/autho")
def authorization():
    return "Authorization"
