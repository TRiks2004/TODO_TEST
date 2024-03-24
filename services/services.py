from sqlalchemy.ext.asyncio import AsyncSession


async def result_execute(stmt, session: AsyncSession):
    result = await session.execute(stmt)
    return result.scalars()
