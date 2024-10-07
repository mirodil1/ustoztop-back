# ruff: noqa: INP001
import logging

import uvicorn as uvicorn
from core import config
from core.logger import LOGGING
from db.postgres import Base, engine
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.api.v1 import announcements, categories
from src.middlewares import JWTAuthBackend
from starlette.middleware.authentication import AuthenticationMiddleware

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())
Base.metadata.create_all(bind=engine)


app.include_router(categories.router, prefix="/v1/categories")
app.include_router(announcements.router, prefix="/v1/announcements")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
