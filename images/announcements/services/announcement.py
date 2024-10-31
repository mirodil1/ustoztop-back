import uuid

import httpx
from core.config import settings
from db.postgres import get_db
from fastapi import Depends
from models.announcement import Announcement
from schemas.announcement import AnnouncementSchema
from slugify import slugify
from sqlalchemy.orm import Session
from src.paginator import paginate_per_page

from services.announcement_filter import AnnouncementFilter


class AnnouncementService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_announcements(
            self,
            filters: AnnouncementFilter,
            page: int,
            per_page: int,
    ) -> list[AnnouncementSchema]:
        announcements = await self._get_active_announcements(filters)
        paginated_categories = await paginate_per_page(announcements, page, per_page)

        return {
            "announcements": paginated_categories["items"],
            "count": paginated_categories["count"],
            "next_page": paginated_categories["next_page"],
            "previous_page": paginated_categories["previous_page"],
        }

    async def get_announcement_by_slug(self, slug: str, user_agent: str) -> AnnouncementSchema:
        active = await self._get_active_announcements()
        announcement = active.filter(Announcement.slug==slug).scalar()
        if announcement:
            await self._add_views(announcement.id, user_agent)
        return announcement

    async def get_announcement_by_category(
        self,
        category_id: int,
    ) -> list[AnnouncementSchema]:
        active = await self._get_active_announcements()
        announcements = active.filter(Announcement.category_id==category_id).all()
        return announcements

    async def create_announcement(self, user_id: int, data: dict):
        # TODO: check for category existence by its id

        slug = f"{slugify(data.get('name'))}-{uuid.uuid4().hex[:6]}"

        announcement = Announcement(user_id=user_id, slug=slug)
        for key, value in data.items():
            if hasattr(announcement, key):
                setattr(announcement, key, value)
        self.db.add(announcement)
        self.db.commit()

        return announcement

    async def _get_active_announcements(self, filters: AnnouncementFilter):
        announcements = (
            self.db.query(Announcement)
                .filter(
                    Announcement.is_active==True,
                    Announcement.is_confirmed_by_admin==True,
                )
        )
        user_gender = filters.gender
        role_name = filters.role

        filters.gender = None
        filters.role = None

        query = filters.filter(announcements)

        if user_gender or role_name:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.user_url}/api/v1/users/get/idx?gender={user_gender if user_gender else ''}&role={role_name if user_gender else ''}",
                )
                users = response.json()
                user_ids = []
                if response.status_code == 200:
                    user_ids = [user["id"] for user in users]
                query = query.filter(Announcement.user_id.in_(user_ids))
        return query

    async def _add_views(self, announcement_id: int, user_agent: str):
        """
        Requesting to statistics service to add new views
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.stat_url}/v1/statistics/announcement_views/create/{announcement_id}",
                headers={"user-agent": user_agent}
            )
        return response


def get_announcement_service(db: Session = Depends(get_db)) -> AnnouncementService:
    return AnnouncementService(db)
