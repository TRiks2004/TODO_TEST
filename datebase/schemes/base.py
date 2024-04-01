from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar('T')


class BaseModelS(BaseModel):

    # return await RepositoryRole.add(Role(**role.model_dump()))
    def get_model_data(self, model: T) -> T:
        return model(**self.model_dump())
