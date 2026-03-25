from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database.init_db import init_db

from app.routers.user_routes import router as user_router
from app.auth.routes import router as auth_router
from app.routers.health import router as health_router

from app.middlewares.logging_middleware import LoggingMiddleware
from app.middlewares.error_middleware import ErrorMiddleware

from app.core.logging_config import setup_logging
from fastapi.middleware.cors import CORSMiddleware
from app.routers.analytics_routes import router as analytics_routes
from app.routers import insight_routes

# configuration log (before anything else)
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


# Middlewares (correct order)
app.add_middleware(ErrorMiddleware)
app.add_middleware(LoggingMiddleware)

# CORS (basic production-ready)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(auth_router)     # Auth
app.include_router(user_router)     # Users
app.include_router(health_router)   # Health
app.include_router(analytics_routes)
app.include_router(insight_routes.router)

@app.get("/")
def root():
    return {"message": "API running"}