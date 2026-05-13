# routers/api.py
from fastapi import APIRouter

from routers.auth import router as auth_router
from routers.branches import router as branches_router
from routers.users import router as users_router
from routers.products import router as products_router
from routers.stock import router as stock_router
from routers.sales import router as sales_router
from routers.stock_requests import router as stock_requests_router
from routers.ws import router as ws_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(branches_router)
api_router.include_router(users_router)
api_router.include_router(products_router)
api_router.include_router(stock_router)
api_router.include_router(sales_router)
api_router.include_router(stock_requests_router)
api_router.include_router(ws_router)
