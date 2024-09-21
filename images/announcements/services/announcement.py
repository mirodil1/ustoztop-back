from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session, joinedload

from db.postgres import get_db
from models.announcement import Announcement
from models.category import Category
from schemas.announcement import AnnouncementSchema


class AnnouncementService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_announcements(self, language: str):
        announcements = (
            self.db.query(Announcement)
                .options(
                    joinedload(Announcement.category),
                )
                .filter(
                    Announcement.is_active==True,
                    Announcement.is_confirmed_by_admin==True
                )
        )

        return announcements
    
    async def get_announcement_by_id(self, announcement_id: int):
        pass

    async def get_announcement_by_category(self, category_id: int):
        pass

    async def create_announcement(self):
        pass


def get_announcement_service(db: Session = Depends(get_db)) -> AnnouncementService:
    return AnnouncementService(db)
