from .model.role import RepositoryRoleServices

from exception import (
    NoRoleExistsHttpException,
    TokenNotFoundHttpException,
    DeniedAccessException,
)


class AccessLevels:

    noToken = None

    # -- Access Levels Defult (0 - 9) --
    lavel_defult = list(range(0, 10))

    defult = 0
    user = 3
    admin = 7

    # -- Access Levels Ultimate (10 - 15) --
    lavel_ultimate = list(range(10, 16))

    @classmethod
    async def check(cls, access_level: int, access_level_check: int):

        if access_level in cls.lavel_defult:
            return access_level <= access_level_check

        elif access_level in cls.lavel_ultimate:
            return access_level == access_level_check

        else:
            raise NoRoleExistsHttpException("Роль не найдена")


async def check_access_level(token: str | None, access_level: int | None):

    if access_level is None:
        return

    if token is None:
        raise TokenNotFoundHttpException("Токен не найден")

    check_lavel = await RepositoryRoleServices.get_lavel_by_token(token)

    if check_lavel is not None:
        access = await AccessLevels.check(access_level, check_lavel)

        if not access:
            raise DeniedAccessException("Доступ запрещен")
    else:
        raise TokenNotFoundHttpException("Токен не найден")
