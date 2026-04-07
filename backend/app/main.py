from dotenv import load_dotenv
load_dotenv()
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
from app.routers.ad_account_routes import router as ad_account_routes
from app.routers.client_routes import router as client_router
from app.routers.kpi_routes import router as kpi_routes
from app.routers.score_routes import router as score_routes
from app.routers.dashboard_routes import router as dashboard_routes
from app.routers.admin_routes import router as admin_router
from app.auth import reauth
from app.routers.subscription_routes import router as subscription_router

from app.services.scheduler import start_scheduler

#(OBRIGATÓRIO PARA OAUTH)
from starlette.middleware.sessions import SessionMiddleware
from app.config.settings import settings

# logging
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    start_scheduler()
    yield


app = FastAPI(lifespan=lifespan)


# =========================
# MIDDLEWARES (ORDEM IMPORTA)
# =========================

# 1. Session (ANTES DE TUDO que usa request)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)

# 2. Error
app.add_middleware(ErrorMiddleware)

# 3. Logging
app.add_middleware(LoggingMiddleware)

# 4. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ROUTERS
# =========================

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(health_router)
app.include_router(analytics_routes)
app.include_router(insight_routes.router)
app.include_router(client_router)
app.include_router(ad_account_routes)
app.include_router(kpi_routes)
app.include_router(score_routes)
app.include_router(dashboard_routes)
app.include_router(admin_router)
app.include_router(reauth.router)
app.include_router(subscription_router)

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"message": "API running"}