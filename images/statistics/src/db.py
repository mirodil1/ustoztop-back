from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(settings.mongodb_url)
database = client[settings.mongodb_db]


# Define collections
phone_views_collection = database["PhoneNumberViews"]
announcement_views_collection = database["AnnouncementViews"]
account_views_collection = database["AccountViews"]
