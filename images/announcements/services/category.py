from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session, joinedload

from db.postgres import get_db
from models.category import Category
from schemas.category import CategorySchema


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


@lru_cache
def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)
