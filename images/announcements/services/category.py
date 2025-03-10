from functools import lru_cache

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from db.postgres import get_db
from src.paginator import paginate_per_page
from models.category import Category
from models.announcement import Announcement
from schemas.category import CategorySchema


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_categories(self, language: str, page: int, per_page: int):
        # Subquery to count announcements for each child category
        announcement_count_subquery = (
            self.db.query(
                Announcement.category_id,
                func.count(Announcement.id).label("announcement_count")
            )
            .group_by(Announcement.category_id)
            .subquery()
        )
        parent_count_subquery = (
            self.db.query(
                Category.parent_id.label("parent_id"),
                func.coalesce(func.sum(announcement_count_subquery.c.announcement_count), 0).label("announcement_count")
            )
            .join(announcement_count_subquery, Category.id == announcement_count_subquery.c.category_id, isouter=True)
            .group_by(Category.parent_id)
            .subquery()
        )
        # Main query to fetch parent categories with aggregated announcement count
        categories = (
            self.db.query(
                Category,
                func.coalesce(parent_count_subquery.c.announcement_count, 0).label("announcement_count")
            )
            .outerjoin(parent_count_subquery, Category.id == parent_count_subquery.c.parent_id)
            .filter(Category.parent_id.is_(None))  # Only top-level (parent) categories
            .options(
                joinedload(Category.translations),
                joinedload(Category.children).joinedload(Category.translations),
            )
            .order_by(Category.order)
        )
        paginated_categories = await paginate_per_page(categories, page, per_page)
        category_list = []

        for category, announcement_count in categories:
            category.announcement_count = announcement_count  # Dynamically add the field
            category_list.append(category)

        translated_categories = [
            CategorySchema.model_validate(category).model_dump(language=language)
            for category in category_list
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
