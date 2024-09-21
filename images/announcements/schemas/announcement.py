from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

import orjson
from pydantic import BaseModel

# from sqlalchemy import Enum


class LessonTypeEnum(str, Enum):
    GROUP = "group"
    INDIVIDUAL = "individual"


class LessonPlaceEnum(str, Enum):
    ONLINE = "online"
    IN_PERSON = "in_person"


class LessonLanguageEnum(str, Enum):
    UZ = "uz"
    RU = "ru"
    EN = "en"


class LessonAudienceEnum(str, Enum):
    CHILDREN = "children"
    ADULTS = "adults"
    ALL = "all"


class AnnouncementSchema(BaseModel):
    id: Optional[int]
    name: str
    slug: str  
    user_id: int  
    phone_number: str
    price: Decimal
    lessons_in_week: int
    lesson_duration_hours: int
    lesson_type: LessonTypeEnum
    lesson_place: LessonPlaceEnum
    lesson_language: LessonLanguageEnum
    lesson_audience: LessonAudienceEnum
    description: str
    is_active: bool = False
    is_confirmed_by_admin: bool = False
    is_promoted: bool = False
    promotion_started: Optional[date]
    promotion_expired: Optional[date]
    category_id: int

    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson.dumps
