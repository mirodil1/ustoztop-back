from datetime import date, datetime

from pydantic import BaseModel, validator


class BaseViews(BaseModel):
    id: str
    user_data: str
    created_at: date

    @validator("created_at", pre=True)
    def string_to_date(cls, v: object) -> object:
        if isinstance(v, datetime):
            return v.date()
        return v


class AnnouncementViews(BaseViews):
    announcement_id: int


class ProfileViews(BaseViews):
    user_id: int


class PhoneNumberViews(BaseViews):
    announcement_id: int
    phone_number: str
