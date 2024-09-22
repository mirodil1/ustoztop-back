import enum
from datetime import date
from decimal import Decimal
from typing import Optional

import orjson
from pydantic import BaseModel
from sqlalchemy import Enum

from schemas.category import CategorySchema


class LessonTypeEnum(enum.Enum):
    group = "group"
    individual = "individual"


class LessonPlaceEnum(enum.Enum):
    online = "online"
    in_person = "in_person"


class LessonLanguageEnum(enum.Enum):
    uz = "uz"
    ru = "ru"
    en = "en"


class LessonAudienceEnum(enum.Enum):
    children = "children"
    adults = "adults"
    all = "all"


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


class AnnouncementOutputSchema(BaseModel):
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
    is_promoted: bool = False
    promotion_started: Optional[date]
    promotion_expired: Optional[date]
    category: CategorySchema