from datebase.connect import async_session_maker


def async_session_decorator(func):
    async def wrapper(*args, **kwargs):
        if kwargs.get("session", None) is None:
            async with async_session_maker() as session:
                kwargs["session"] = session
                print("Генерирована сессия")
                return await func(*args, **kwargs)
        else:
            print("Существует сессия")
            return await func(*args, **kwargs)

    return wrapper
