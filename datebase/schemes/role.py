from pydantic import BaseModel


from typing import Generic, TypeVar

T = TypeVar("T")


class BaseModelS(BaseModel):

    # return await RepositoryRole.add(Role(**role.model_dump()))
    def get_model_data(self, model: T) -> T:
        return model(**self.model_dump())


from datebase.models import Role


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
