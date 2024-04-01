from pydantic_settings import BaseSettings


class Prefix(BaseSettings):
    identification: str = 'identification'
    user: str = 'user'
    role: str = 'role'


prefix = Prefix()
