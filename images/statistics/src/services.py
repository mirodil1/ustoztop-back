from datetime import datetime

from src.db import (
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
                        {
                "announcement_id": announcement_id,
                "user_data": "data",
                "created_at": datetime.now()
            }

        )
        return result
    
    @staticmethod
    async def get_announcement_views(announcement_id: int):
        results = [views async for views in phone_views_collection.find({"announcement_id": announcement_id})]
        return results



async def get_announcement_stat_service():
    return AnnouncementViewsService()