from datebase.models import Role

from .base import BaseModelS


class BaseRoleS(BaseModelS):
    name: str
    lavel: int | None = None

    def get_model_data(self):
        return super().get_model_data(Role)

    class Config:
        from_attributes = True


class CreateRoleS(BaseRoleS):
    pass


class GetRoleS(BaseRoleS):
    id_role: int
