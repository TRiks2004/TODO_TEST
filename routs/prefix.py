from pydantic_settings import BaseSettings

class Prefix(BaseSettings):
    identification: str = '/identification'
    
prefix = Prefix()