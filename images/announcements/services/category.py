from functools import lru_cache

from db.postgres import get_db
from fastapi import Depends
from models.category import Category
from schemas.category import CategorySchema
from sqlalchemy.orm import Session, joinedload
from src.paginator import paginate_per_page


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_categories(self, language: str, page: int, per_page: int):
        categories = (
            self.db.query(Category)
                .options(
                    joinedload(Category.translations),
                    joinedload(Category.parent),
                )
                .filter(Category.parent_id.is_(None))
        )
        paginated_categories = await paginate_per_page(categories, page, per_page)

        translated_categories = [
            CategorySchema.model_validate(category).model_dump(language=language)
            for category in paginated_categories["items"]
        ]
        return {
            "categories": translated_categories,
            "count": paginated_categories["count"],
            "next_page": paginated_categories["next_page"],
            "previous_page": paginated_categories["previous_page"],
        }

    async def get_category_by_id(
            self,
            category_id: int,
            language: str,
    ) -> CategorySchema | None:
        category = self.db.query(Category).filter(Category.id==category_id).scalar()
        if category:
            return CategorySchema.model_validate(category).model_dump(language=language)
        return None

@lru_cache
def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)
