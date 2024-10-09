from functools import lru_cache
from typing import Optional

from db.postgres import get_db
from fastapi import Depends
from models.category import Category
from schemas.category import CategorySchema
from sqlalchemy.orm import Session, joinedload


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_categories(self, language: str):
        categories = (
            self.db.query(Category)
                .options(
                    joinedload(Category.translations),
                    joinedload(Category.parent),
                )
                .filter(Category.parent_id.is_(None))
        )
        translated_categories = [
            CategorySchema.model_validate(category).model_dump(language=language)
            for category in categories
        ]
        return translated_categories

    async def get_category_by_id(
            self, category_id: int, language: str
    ) -> CategorySchema | None:
        category = self.db.query(Category).filter(Category.id==category_id).scalar()
        if category:
            return CategorySchema.model_validate(category).model_dump(language=language)
        return None

@lru_cache
def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)
