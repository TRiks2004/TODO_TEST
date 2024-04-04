from fastapi import FastAPI

# подключение настроек
from common import settings_api

# подключение сразу всех роутов
from routs import include_routers

# подключение кэша
from datebase import init_fast_api_cache

from datebase.connect import test_db

from tools.test import MinioClient


async def lifespan(app: FastAPI):
    ml_models = {}

    await MinioClient.get_instance()

    await init_fast_api_cache()
    await test_db()

    yield ml_models


def create_app() -> FastAPI:
    app = FastAPI(
        debug=settings_api.debug,
        docs_url="/docs",
        title="SUAI Schedule API(FastAPI)",
        lifespan=lifespan,
    )

    include_routers(app)

    return app
