from fastapi import FastAPI
from app.routers import health

app = FastAPI(
    title="InsightFlow API",
    version="1.0.0",
    description="Marketing Analytics SaaS API"
)

app.include_router(health.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "InsightFlow API is running!"}