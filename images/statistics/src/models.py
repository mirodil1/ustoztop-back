from datetime import datetime

from pydantic import BaseModel


class AnnouncementViews(BaseModel):
    announcement_id: int
    user_data: str
    created_at: datetime


class ProfileViews(BaseModel):
    user_id: int
    user_data: str
    created_at: datetime


class PhoneNumberViews(BaseModel):
    announcement_id: int
    phone_number: str
    user_data: str
    created_at: datetime
