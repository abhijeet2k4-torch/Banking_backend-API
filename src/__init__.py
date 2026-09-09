from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.main import init_db
from src.accounts.routes import router as accounts_router
from src.users.routes import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
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
app.include_router(users_router, prefix="/users", tags=['users'])
app.include_router(accounts_router, prefix="/accounts", tags=['accounts'])