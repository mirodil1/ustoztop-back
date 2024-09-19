from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, joinedload
from starlette import status
from starlette.responses import RedirectResponse

from db.postgres import get_db
from models.category import Category
from schemas.category import CategoryOutputSchema, CategorySchema

router = APIRouter(
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_categories(db: Session = Depends(get_db)):
    data = (
        db.query(Category)
        .options(
            joinedload(Category.translations),
            joinedload(Category.parent),
        )
        .filter(Category.parent_id.is_(None))
    )

    res = [
        CategorySchema.model_validate(category).model_dump(language="uz")
        for category in data
    ]
    return res
