# ruff: noqa: INP001
import logging

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from src.api import v1
from src.middlewares import JWTAuthBackend
from core.config import settings
from core.logger import LOGGING

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/v1/statistics/openapi",
    openapi_url="/api/v1/statistics/openapi.json",
)

app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1.router, prefix="/api/v1/statistics")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8081,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=settings.debug,
    )
