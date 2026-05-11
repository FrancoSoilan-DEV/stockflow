# routers/api.py
from fastapi import APIRouter

from routers.auth import router as auth_router
from routers.branches import router as branches_router
from routers.users import router as users_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(branches_router)
api_router.include_router(users_router)

