from typing import TypeVar, Generic
from .RepositoryModel import RepositoryModel

RMT = TypeVar("RMT", bound=RepositoryModel)


class RepositoryModelServices(Generic[RMT]):
    _RMD: RMT = RMT

    def __init__(self) -> None:
        pass
