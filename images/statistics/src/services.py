from datetime import datetime

from db import (
    account_views_collection,
    announcement_views_collection,
    phone_views_collection,
)


class PhoneNumberViewsService:
    pass


class AnnouncementViewsService:

    @staticmethod
    async def create_announcement_views(announcement_id: int):
        result = await phone_views_collection.insert_one(
            announcement_id=announcement_id,
            user_data="data",
            created_at=datetime.now(),
        )
        return result
