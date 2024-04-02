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


from repository.access_levels import AccessLevels, check_access_level


async def main():

    await check_access_level(
        "XD5TrqCebIUI2X4xhS4otxAPUhTyg27QhIVXk9fZi6y8Htx0xFleB9hsuzwJ1ZN3HyTHDliu02WHPq1ZsoqHcNkYMLISZCEjEtp2",
        AccessLevels.defult,
    )


asyncio.run(main())
