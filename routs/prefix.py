from pydantic_settings import BaseSettings

class Prefix(BaseSettings):
    identification: str = 'identification'
    user: str = 'user'
    
prefix = Prefix()