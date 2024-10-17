# ruff: noqa: INP001
import logging

import uvicorn as uvicorn
from core import config
from core.logger import LOGGING
from fastapi import FastAPI

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8081,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
