import uuid

import httpx
from core.config import settings
from db.postgres import get_db
from fastapi import Depends
from models.announcement import Announcement
from schemas.announcement import AnnouncementSchema
from slugify import slugify
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from services.announcement_filter import AnnouncementFilter


class AnnouncementService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_announcements(self, filters: AnnouncementFilter) -> list[AnnouncementSchema]:
        announcements = await self._get_active_announcements(filters)
        return announcements.all()

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
        query = filters.filter(announcements)
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
