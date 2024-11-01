from datetime import datetime, timedelta

from src.db import (
    account_views_collection,
    announcement_views_collection,
    phone_views_collection,
)


class PhoneNumberViewsService:
    pass


class AccountViewsService:
    @staticmethod
    async def create_account_views(user_id: int, data: str | None):
        result = await account_views_collection.insert_one(
            {
                "user_id": user_id,
                "user_data": data,
                "created_at": datetime.now(),
            },
        )
        return result

    @staticmethod
    async def get_account_views(user_id: int):
        account_views = []
        last_30 = datetime.now() - timedelta(days=30)
        async for view in account_views_collection.find(
            {
                "user_id":user_id,
                "created_at": {"$gte": last_30},
            },
        ):
            # Convert MongoDB ObjectId to string for serialization
            view["id"] = str(view["_id"])
            account_views.append(view)
        return account_views


async def get_account_stat_service():
    return AccountViewsService()


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
        pipeline = [
            {
                "$match": {
                    "announcement_id": announcement_id,
                    "created_at": {"$gte": last_30},
                },
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"},
                    },
                    "count": {"$sum": 1},
                },
            },
            {
                "$project": {
                    "date": "$_id",
                    "count": 1,
                    "_id": 0,
                },
            },
            {
                "$sort": {"date": 1},  # Sort by date ascending
            },
        ]
        async for view in announcement_views_collection.aggregate(
            pipeline,
        ):
            # Convert MongoDB ObjectId to string for serialization
            # view["id"] = str(view["_id"])
            announcement_views.append(view)

        return announcement_views


async def get_announcement_stat_service():
    return AnnouncementViewsService()
