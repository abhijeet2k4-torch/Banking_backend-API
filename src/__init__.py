from fastapi import FastAPI, status
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Server is starting up...")
    await init_db()
    yield
    print("Server is shutting down...")

app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)
version = "v1"