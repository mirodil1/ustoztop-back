# ruff: noqa: INP001
import os
import logging

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core import config
from core.logger import LOGGING
from src.api.v1 import announcements

from db.postgres import Base
from db.postgres import engine


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

Base.metadata.create_all(bind=engine)


app.include_router(announcements.router, prefix='/v1/announcements', tags=['announcement'])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True
    )   
# models.Base.metadata.create_all(bind=engine)