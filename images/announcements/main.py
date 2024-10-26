# ruff: noqa: INP001
import logging

import uvicorn as uvicorn
from core.config import settings
from core.logger import LOGGING
from db.postgres import Base, engine
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.api.v1 import announcements, categories
from src.middlewares import JWTAuthBackend
from starlette.middleware.authentication import AuthenticationMiddleware

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/v1/announcements/openapi",
    openapi_url="/api/v1/announcements/openapi.json",
    default_response_class=ORJSONResponse,
)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())
Base.metadata.create_all(bind=engine)


app.include_router(categories.router, prefix="/api/v1/announcements/categories")
app.include_router(announcements.router, prefix="/api/v1/announcements")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
