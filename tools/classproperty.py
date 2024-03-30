from typing import TypeVar


class classproperty(object):

    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__

    def __get__(self, instance, owner):
        return classmethod(self.func).__get__(None, owner)()
