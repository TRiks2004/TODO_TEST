from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_session,
    AsyncSession,
)
from sqlalchemy import text, insert
from common import settings_database

engine_async = create_async_engine(
    url=settings_database.db_url_async,
    echo=settings_database.db_debug,
)

async_session_maker = async_sessionmaker(engine_async, expire_on_commit=False)


async def get_async_session() -> AsyncSession:  # type: ignore
    async with async_session_maker() as session:
        yield session


def async_db_transaction(engine_async=engine_async):
    """
    Decorator to manage database connection and transaction for an asynchronous function.
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            async with engine_async.begin() as conn:
                # Pass the connection object to the decorated function
                await func(conn, *args, **kwargs)

        return wrapper

    return decorator


# Define an asynchronous function to test the database
@async_db_transaction()
async def test_db(conn) -> None:
    rez = await conn.execute(text("SELECT 1"))
    print("tr = ", rez.fetchall())  # Print the result of the query
