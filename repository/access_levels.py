from .model.role import RepositoryRoleServices 




class AccessLevels:
    
    noToken = None
        
    # -- Access Levels Defult (0 - 9) --
    defult = 0
    user = 3
    admin = 7
    
    # -- Access Levels Ultimate (10 - 15) --
    
    @classmethod
    async def check(cls, access_level: int, access_level_check: int):
        
        return access_level <= access_level_check
    


async def check_access_level(token: str | None, access_level: int | None):
    
    if access_level is None:
        return
    
    if token is None:
        raise Exception("Токен не найден")
    
    check_lavel = await RepositoryRoleServices.get_lavel_by_token(token)
    
    if check_lavel is not None:
        access = await AccessLevels.check(access_level, check_lavel)
        
        if not access:
            raise Exception("Доступ запрещен")
        
    else:
        raise Exception("Токен не найден") # TODO: Сделать обработку ошибки













