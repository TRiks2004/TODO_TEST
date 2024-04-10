

from routs.prefix import TokenSchema


class FastApiTest:
    def __init__(self, access_level='default'):
        self.access_level = access_level

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            token = kwargs.get('token')  # Получить токен из аргументов, если он передан
            print(f"Checking access level '{self.access_level}' with token: {token}")
            return func(*args, **kwargs)
        return wrapper


# @FastApiTest.check_access_level(token="token", access_level='default')
# def test():
#     return 1

# test()













