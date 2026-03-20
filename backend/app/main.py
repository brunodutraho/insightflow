from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database.init_db import init_db
from app.routers.user_routes import router as user_router
from app.auth.routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

# routers
app.include_router(auth_router)   # Authentication
app.include_router(user_router)   # Users


@app.get("/")
def root():
    return {"message": "API running"}