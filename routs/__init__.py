from fastapi import FastAPI, APIRouter

from .identification import identification_router
from .role import role_router
from .user import user_router


def include_router(app: FastAPI, router: APIRouter):
    app.include_router(router)


def include_routers(app: FastAPI):
    routers = [user_router, role_router, identification_router]

    for router in routers:
        include_router(app, router)
