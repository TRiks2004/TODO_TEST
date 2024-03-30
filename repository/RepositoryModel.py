from sqlalchemy import ColumnElement, Executable, Sequence, delete, update

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sqlalchemy.orm.attributes import InstrumentedAttribute

from datebase.models import BaseModel

from typing import Generic, TypeVar, Union, Iterator

from tools.classproperty import classproperty

from .utilities import async_session_decorator


MDT = TypeVar("MDT", bound=BaseModel)
"""Model Data Type - тип данных модели данных"""


class RepositoryModel(Generic[MDT]):
    # Переменная класса для хранения типа модели данных
    _MDB: MDT
    """Model Data Base - Модель данных для репозитория"""

    def __init__(self):
        pass

    @classmethod
    @async_session_decorator
    async def add(
        cls,
        model: MDT,
        *,
        session: AsyncSession = None,
    ) -> MDT:
        """Метод для добавления новой модели в базу данных."""

        # Добавление модели в сессию
        session.add(model)
        # Применение изменений
        await session.flush()
        # Фиксация изменений
        await session.commit()
        return model

    @classmethod
    @async_session_decorator
    async def get(
        cls,
        whereclause: ColumnElement[bool],
        *,
        session: AsyncSession = None,
    ) -> MDT:
        """Метод для получения модели из базы данных по условию."""

        # Формирование запроса
        stmt = select(cls._MDB).where(whereclause)
        # Выполнение запроса
        result = await session.execute(stmt)
        # Возвращение результата
        return result.scalars().one_or_none()

    @classmethod
    @async_session_decorator
    async def get_column(
        cls,
        whereclause: ColumnElement[bool],
        *args: InstrumentedAttribute,
        session: AsyncSession = None,
    ) -> str | None:
        print(args)
        print(type(args))
        # Формирование запроса
        stmt = select(*args).where(whereclause)
        # Выполнение запроса
        result = await session.execute(stmt)
        # Возвращение результата
        return result.scalars().one_or_none()

    @classmethod
    @async_session_decorator
    async def get_all(
        cls, skip: int = 0, limit: int = 100, *, session: AsyncSession = None
    ) -> Iterator[MDT]:
        """Метод для получения всех моделей из базы данных с пагинацией."""

        # Формирование запроса на получение всех моделей
        stmt = select(cls._MDB).offset(skip).limit(limit)
        # Выполнение запроса
        result = await session.execute(stmt)
        # Возвращение списка всех моделей
        return list(result.scalars().all())

    @classmethod
    @async_session_decorator
    async def update(
        cls,
        whereclause: ColumnElement[bool],
        *args: Union[Executable, Sequence],
        session: AsyncSession = None,
    ) -> MDT:
        """Метод для обновления модели в базе данных по условию."""

        # Формирование запроса на обновление
        stmt = (
            update(cls._MDB)
            .values(*args)
            .where(whereclause)
            .returning(cls._MDB)
        )
        # Выполнение запроса
        result = await session.execute(stmt)

        # Применение изменений
        await session.flush()
        # Фиксация изменений
        await session.commit()

        return result.scalars().one_or_none()

    @classmethod
    @async_session_decorator
    async def delete(
        cls,
        whereclause: ColumnElement[bool],
        *,
        session: AsyncSession = None,
    ) -> MDT:
        """Метод для удаления модели из базы данных по условию."""

        # Формирование запроса на удаление
        stmt = delete(cls._MDB).where(whereclause).returning(cls._MDB)
        # Выполнение запроса
        result = await session.execute(stmt)

        # Применение изменений
        await session.flush()
        # Фиксация изменений
        await session.commit()

        return result.scalars().one_or_none()
