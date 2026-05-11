# main.py
from fastapi import FastAPI

from routers.api import api_router

app = FastAPI(title="Stockflow API")

app.include_router(api_router)


@app.get("/")
async def home():
    return {"message": "Stockflow API corriendo"}