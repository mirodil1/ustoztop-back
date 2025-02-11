from datetime import date, datetime

from pydantic import BaseModel, validator


class BaseViews(BaseModel):
    count: int
    date: date

    @validator("date", pre=True)
    def string_to_date(cls, v: object) -> object:
        if isinstance(v, datetime):
            return v.date()
        return v


class AnnouncementViews(BaseViews):
    pass


class ProfileViews(BaseViews):
    pass


class PhoneNumberViews(BaseModel):
    count: int
