import uuid

from db.postgres import get_db
from fastapi import Depends
from models.announcement import Announcement
from schemas.announcement import AnnouncementSchema
from slugify import slugify
from sqlalchemy.orm import Session


class AnnouncementService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_announcements(self) -> list[AnnouncementSchema]:
        announcements = await self._get_active_announcements()
        return announcements.all()

    async def get_announcement_by_slug(self, slug: str) -> AnnouncementSchema:
        active = await self._get_active_announcements()
        announcement = active.filter(Announcement.slug==slug).scalar()
        return announcement

    async def get_announcement_by_category(
        self,
        category_id: int,
    ) -> list[AnnouncementSchema]:
        active = await self._get_active_announcements()
        announcements = active.filter(Announcement.category_id==category_id).all()
        return announcements

    async def create_announcement(self, user_id: int, data: dict):
        # TODO: check category existence by its id

        slug = f"{slugify(data.get('name'))}-{uuid.uuid4().hex[:6]}"

        announcement = Announcement(user_id=user_id, slug=slug)
        for key, value in data.items():
            if hasattr(announcement, key):
                setattr(announcement, key, value)
        self.db.add(announcement)
        self.db.commit()

        return announcement

    async def _get_active_announcements(self):
        announcements = (
            self.db.query(Announcement)
                .filter(
                    Announcement.is_active==True,
                    Announcement.is_confirmed_by_admin==True,
                )
        )
        return announcements


def get_announcement_service(db: Session = Depends(get_db)) -> AnnouncementService:
    return AnnouncementService(db)
