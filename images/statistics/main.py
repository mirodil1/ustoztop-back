# ruff: noqa: INP001
import logging

import uvicorn as uvicorn
from core.config import settings
from core.logger import LOGGING
from src.api import v1
from fastapi import FastAPI

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

app.include_router(v1.router, prefix="/v1/statistics")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8081,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
