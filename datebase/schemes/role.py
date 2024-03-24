from pydantic import BaseModel

class BaseRole(BaseModel):
    id_role: int
    name: str
    lavel: int
    
    class Config:
        from_attributes = True

class CreateRole(BaseRole):
    pass

class GetRole(BaseRole):
    pass

