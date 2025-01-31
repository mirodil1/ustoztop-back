# ruff: noqa: INP001
import logging

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware
from debug_toolbar.middleware import DebugToolbarMiddleware

from core.config import settings
from core.logger import LOGGING
from db.postgres import Base, engine
from src.api.v1 import announcements, categories, core
from src.api.v1 import plans
from src.middlewares import JWTAuthBackend, PaginationMiddleware

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/v1/announcements/openapi",
    openapi_url="/api/v1/announcements/openapi.json",
    default_response_class=ORJSONResponse,
    debug=settings.debug
)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(PaginationMiddleware)

if settings.debug:
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["db.postgres.SQLAlchemyPanel"],
    )

Base.metadata.create_all(bind=engine)

app.include_router(announcements.router, prefix="/api/v1/announcements")
app.include_router(plans.router, prefix="/api/v1/plans")
app.include_router(categories.router, prefix="/api/v1/categories")
app.include_router(core.router, prefix="/api/v1/regions")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=settings.debug,
    )
