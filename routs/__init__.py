from fastapi import FastAPI, APIRouter

from .user import user_router
from .role import role_router
from .identification import identification_router

from .file import file_router


def include_router(app: FastAPI, router: APIRouter):
    app.include_router(router)


def include_routers(app: FastAPI):
    routers = [user_router, role_router, identification_router, file_router]

    for router in routers:
        include_router(app, router)
