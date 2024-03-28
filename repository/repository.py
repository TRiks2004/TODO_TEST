from sqlalchemy import ColumnElement, Executable, Sequence, delete, update

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from datebase.connect import async_session_maker
from datebase.models import BaseModel

from typing import Generic, TypeVar, Union, Iterator

MDT = TypeVar("MDT", bound=BaseModel)
"""Model Data Type - тип данных модели данных"""


class Repository(Generic[MDT]):
    # Переменная класса для хранения типа модели данных
    MDB: MDT
    """Модель Data Base - Модель данных для репозитория"""

    def __init__(self):
        pass

    @staticmethod
    def with_async_session(func):
        """Декоратор для обеспечения использования асинхронной сессии SQLAlchemy."""

        # Объявление обертки для асинхронного вызова функции
        async def wrapper(cls, *args, **kwargs):
            # Создание асинхронной сессии
            async with async_session_maker() as session:
                # Передача сессии как аргумента и вызов исходной функции
                kwargs["session"] = session
                return await func(cls, *args, **kwargs)

        return wrapper

    @classmethod
    @with_async_session
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
    @with_async_session
    async def get(
        cls,
        whereclause: ColumnElement[bool],
        *,
        session: AsyncSession = None,
    ) -> MDT:
        """Метод для получения модели из базы данных по условию."""

        # Формирование запроса
        stmt = select(cls.MDB).where(whereclause)
        # Выполнение запроса
        result = await session.execute(stmt)
        # Возвращение результата
        return result.scalars().one_or_none()

    @classmethod
    @with_async_session
    async def update(
        cls,
        whereclause: ColumnElement[bool],
        *args: Union[Executable, Sequence],
        session: AsyncSession = None,
    ) -> MDT:
        """Метод для обновления модели в базе данных по условию."""

        # Формирование запроса на обновление
        stmt = (
            update(cls.MDB).values(*args).where(whereclause).returning(cls.MDB)
        )
        # Выполнение запроса
        result = await session.execute(stmt)

        # Применение изменений
        await session.flush()
        # Фиксация изменений
        await session.commit()

        return result.scalars().one_or_none()

    @classmethod
    @with_async_session
    async def delete(
        cls,
        whereclause: ColumnElement[bool],
        *,
        session: AsyncSession = None,
    ) -> MDT:
        """Метод для удаления модели из базы данных по условию."""

        # Формирование запроса на удаление
        stmt = delete(cls.MDB).where(whereclause).returning(cls.MDB)
        # Выполнение запроса
        result = await session.execute(stmt)

        # Применение изменений
        await session.flush()
        # Фиксация изменений
        await session.commit()

        return result.scalars().one_or_none()

    @classmethod
    @with_async_session
    async def get_all(
        cls, skip: int = 0, limit: int = 100, *, session: AsyncSession = None
    ) -> Iterator[MDT]:
        """Метод для получения всех моделей из базы данных с пагинацией."""

        # Формирование запроса на получение всех моделей
        stmt = select(cls.MDB).offset(skip).limit(limit)
        # Выполнение запроса
        result = await session.execute(stmt)
        # Возвращение списка всех моделей
        return list(result.scalars().all())
