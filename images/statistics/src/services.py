from datetime import datetime, timedelta

from src.db import (
    account_views_collection,
    announcement_views_collection,
    phone_views_collection,
)


class PhoneNumberViewsService:

    @staticmethod
    async def create_phone_number_views(announcment_id: int, data: str | None):
        result = await phone_views_collection.insert_one(
            {
                "announcement_id": announcment_id,
                "user_data": data,
                "created_at": datetime.now(),
            },
        )
        return result

    @staticmethod
    async def get_phone_number_count(announcement_id: int):
        pipeline = [
            {
                "$match": {
                    "announcement_id": announcement_id,
                },
            },
            {
                "$group": {
                    "_id": "$announcement_id",
                    "count": {"$sum": 1},
                },
            },
            {
                "$project": {
                    "_id": 0,
                    "count": 1,
                },
            },
        ]
        count = (
            await phone_views_collection.aggregate(pipeline).to_list(length=None)
        )
        if not count:
            return {"count": 0}
        return count[0]


async def get_phone_number_stat_service() -> PhoneNumberViewsService:
    return PhoneNumberViewsService()


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
        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
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
        async for view in account_views_collection.aggregate(
            pipeline,
        ):
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
    async def get_views_count_by_id(announcement_id: int):
        pipeline = [
            {
                "$match": {
                    "announcement_id": announcement_id,
                },
            },
            {
                "$group": {
                    "_id": "$announcement_id",
                    "count": {"$sum": 1},
                },
            },
            {
                "$project": {
                    "_id": 0,
                    "count": 1,
                },
            },
        ]
        count = (
            await announcement_views_collection.aggregate(pipeline).to_list(length=None)
        )
        if not count:
            return {"count": 0}
        return count[0]


    @staticmethod
    async def get_last_views(announcement_id: int):
        announcement_views = []
        last_30 = datetime.now() - timedelta(days=365)
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
            announcement_views.append(view)

        return announcement_views


async def get_announcement_stat_service():
    return AnnouncementViewsService()
