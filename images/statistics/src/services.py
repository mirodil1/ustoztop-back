from datetime import datetime, timedelta

from src.db import (
    account_views_collection,
    announcement_views_collection,
    phone_views_collection,
)


class PhoneNumberViewsService:
    pass


class AnnouncementViewsService:

    @staticmethod
    async def create_announcement_views(announcement_id: int, data: str | None):
        result = await announcement_views_collection.insert_one(
            {
                "announcement_id": announcement_id,
                "user_data": data,
                "created_at": datetime.now(),
            },
        )
        return result

    @staticmethod
    async def get_announcement_views(announcement_id: int):
        announcement_views = []
        last_30 = datetime.now() - timedelta(days=30)
        async for view in announcement_views_collection.find(
            {
                "announcement_id":announcement_id,
                "created_at": {"$gte": last_30},
            },
        ):
            # Convert MongoDB ObjectId to string for serialization
            view["id"] = str(view["_id"])
            announcement_views.append(view)
        return announcement_views


async def get_announcement_stat_service():
    return AnnouncementViewsService()
