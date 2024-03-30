from datebase.connect import async_session_maker


def async_session_decorator(func):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            kwargs["session"] = session
            return await func(*args, **kwargs)

    return wrapper
