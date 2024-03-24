from sqlalchemy.ext.asyncio import AsyncSession

from typing import List
from uuid import UUID

from datebase.models import Role, User
from sqlalchemy.future import select

from .services import result_execute




async def select_all_role(
    session: AsyncSession, 
    skip: int = 0, limit: int = 100
) -> List[Role]:
    """
    Асинхронно выбирает все роли из базы данных с помощью запроса SQL.

    Args:
        session (AsyncSession): Объект сессии SQLAlchemy для асинхронных операций.
        skip (int, optional): количество пропускаемых записей. Defaults to 0.
        limit (int, optional): ограничение на количество возвращаемых записей. Defaults to 100.

    Returns:
        List[Role]: Список объектов Role из базы данных.
    """
    stmt = select(Role).offset(skip).limit(limit)
    result = await result_execute(stmt, session)
    return result.all()

async def select_role_by_id(
    session: AsyncSession, 
    id_role: int
) -> Role:
    """
    Асинхронно выбирает одну роль из базы данных по ее идентификатору.

    Args:
        session (AsyncSession): Объект сессии SQLAlchemy для асинхронных операций.
        id_role (int): Идентификатор роли, которую нужно выбрать.

    Returns:
        Role: Объект Role из базы данных.
    """
    stmt = select(Role).where(Role.id_role == id_role)
    result = await result_execute(stmt, session)
    return result.all()

async def select_user(
    session: AsyncSession, 
    skip: int = 0, limit: int = 100
) -> List[User]:
    """
    Асинхронно выбирает всех пользователей из базы данных с помощью запроса SQL.

    Args:
        session (AsyncSession): Объект сессии SQLAlchemy для асинхронных операций.
        skip (int, optional): количество пропускаемых записей. Defaults to 0.
        limit (int, optional): ограничение на количество возвращаемых записей. Defaults to 100.

    Returns:
        List[User]: Список объектов User из базы данных.
    """
    stmt = select(User).offset(skip).limit(limit)
    result = await result_execute(stmt, session)
    return result.all()

async def select_user_by_id(
    session: AsyncSession, 
    id_user: UUID
) -> User:
    """
    Асинхронно выбирает одного пользователя из базы данных по его идентификатору.

    Args:
        session (AsyncSession): Объект сессии SQLAlchemy для асинхронных операций.
        id_user (UUID): Идентификатор пользователя, которому нужно выбрать.

    Returns:
        User: Объект User из базы данных.
    """
    stmt = select(User).where(User.id_user == id_user)
    result = await result_execute(stmt, session)
    return result.all()
    