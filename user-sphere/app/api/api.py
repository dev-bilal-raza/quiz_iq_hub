from fastapi import APIRouter
from app.api.router import auth_route, user_route

api_router = APIRouter()

api_router.include_router(router=user_route.router)
api_router.include_router(router=auth_route.router)
