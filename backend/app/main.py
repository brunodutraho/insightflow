from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # startup
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "API running"}