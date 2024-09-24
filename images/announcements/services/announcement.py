from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from db.postgres import get_db
from models.announcement import Announcement
from schemas.announcement import AnnouncementSchema


class AnnouncementService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_announcements(self) -> List[AnnouncementSchema]:
        announcements = await self._get_active_announcements()
        return announcements.all()

    async def get_announcement_by_slug(self, slug: str):
        active = await self._get_active_announcements()
        announcement = active.filter(Announcement.slug==slug).scalar()
        return announcement

    async def get_announcement_by_category(
        self, 
        category_id: int
    ) -> List[AnnouncementSchema]:
        active = await self._get_active_announcements()
        announcements = active.filter(Announcement.category_id==category_id).all()
        return announcements

    async def create_announcement(self):
        pass

    async def _get_active_announcements(self):
        announcements = (
            self.db.query(Announcement)
                .filter(
                    Announcement.is_active==True,
                    Announcement.is_confirmed_by_admin==True
                )
        )
        return announcements


def get_announcement_service(db: Session = Depends(get_db)) -> AnnouncementService:
    return AnnouncementService(db)
