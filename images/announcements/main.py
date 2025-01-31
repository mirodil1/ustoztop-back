# ruff: noqa: INP001
import logging
import json
from contextlib import contextmanager

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware
from debug_toolbar.middleware import DebugToolbarMiddleware

from core.config import settings
from core.logger import LOGGING
from db.postgres import Base, engine, get_db, SessionLocal
from src.api.v1 import announcements, categories
from src.api.v1 import plans
from models.core import Region
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

@contextmanager
def get_db_session():
    """Properly manage the database session."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def create_region(data, parent_id=None):
    """ Recursively create region and its children """
    with get_db_session() as db:

        region = Region(
            uz=data["uz"],
            ru=data["ru"],
            coords=data["coords"],
            parent_id=parent_id
        )
        db.add(region)
        db.commit()
        db.flush()  # Get region ID for child references

        if "children" in data:
            for child in data["children"]:
                create_region(child, parent_id=region.id)

def insert_regions_from_json(json_file="result_mahalla_copy.json"):
    """ Insert regions data into the database from JSON file """
    db = next(get_db())
    with open(json_file, "r", encoding="utf-8") as file:
        regions_data = json.load(file)
        for region_data in regions_data:
            create_region(region_data)

    db.commit()
    # Base.metadata.create_all(bind=engine)

app.include_router(announcements.router, prefix="/api/v1/announcements")
app.include_router(plans.router, prefix="/api/v1/plans")
app.include_router(categories.router, prefix="/api/v1/categories")

@app.on_event("startup")
def startup_event():
    """ This will run when FastAPI starts """
    print("Running startup tasks...")
    Base.metadata.create_all(engine)  # Ensure tables are created
    insert_regions_from_json()  # Insert JSON data into DB


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=settings.debug,
    )
