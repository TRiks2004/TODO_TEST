import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from repository import RepositoryUser, User
from datebase.models import BaseModel

import asyncio
import json


async def user_to_dict(base_model: BaseModel):
    return await base_model.model_to_dict()


async def users_to_dict(users: list[BaseModel]):
    return [await user_to_dict(user) for user in users]


async def to_json(model):
    return json.dumps(model, indent=4)


async def model_to_json(base_model: BaseModel):
    return await to_json(await user_to_dict(base_model))


async def models_to_json(base_models: list[BaseModel]):
    return await to_json(await users_to_dict(base_models))


async def my_print(handler: str, bady: str):
    handler_new = f"| {handler.upper()} |"

    answer = f"\n| {handler_new:-^120} |"

    print(answer)

    print(f"\n{bady}\n")

    print("-" * len(answer))


async def main():

    user = await RepositoryUser.get_all()
    await my_print("RepositoryUser.get_all()", await models_to_json(user))

    user_by_login = await RepositoryUser.get_by_login("triks1")
    await my_print(
        "RepositoryUser.get_by_login()", await model_to_json(user_by_login)
    )

    user_password_by_login = await RepositoryUser.get_hash_password_by_login(
        "triks1"
    )

    await my_print(
        "RepositoryUser.get_by_login()",
        await to_json({"hash_password": user_password_by_login}),
    )

    user_lavel_by_id = await RepositoryUser.get_lavel_by_id(
        "2a9aef5a-42e9-40ee-94c8-91fd82c5314f"
    )

    await my_print(
        "RepositoryUser.get_lavel_by_id()",
        user_lavel_by_id,
    )

    ...


asyncio.run(main())
