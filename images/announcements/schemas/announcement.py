import enum
import uuid
from datetime import date
from decimal import Decimal

import orjson
from pydantic import BaseModel, Field


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


class AnnouncementStatusEnum(enum.Enum):
    active = "active"
    inactive = "inactive"
    rejected = "rejected"
    waiting = "waiting"


class LocationOutputSchema(BaseModel):
    id: uuid.UUID
    uz: str
    ru: str
    region_id: int
    latitude: float
    longitude: float

    class Config:
        from_attributes = True


class LocationInputSchema(BaseModel):
    uz: str
    ru: str
    region_id: int
    latitude: float
    longitude: float


class AnnouncementSchema(BaseModel):
    id: int | None
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
    status: AnnouncementStatusEnum
    description: str
    is_active: bool = False
    is_confirmed_by_admin: bool = False
    is_promoted: bool = False
    promotion_started: date | None
    promotion_expired: date | None
    category_id: int

    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class AnnouncementOutputSchema(BaseModel):
    id: int
    name: str
    slug: str
    user_id: int
    category_id: int
    price: Decimal
    lessons_in_week: int
    lesson_duration_hours: int
    lesson_type: LessonTypeEnum
    lesson_place: LessonPlaceEnum
    lesson_language: LessonLanguageEnum
    lesson_audience: LessonAudienceEnum
    description: str
    location: LocationOutputSchema | None
    is_promoted: bool = False
    promotion_started: date | None
    promotion_expired: date | None

    class Config:
        from_attributes = True


class AnnouncementInputSchema(BaseModel):
    name: str = Field(max_length=128)
    category_id: int
    phone_number: str = Field(max_length=14)
    price: Decimal = Field(lte=99_000_000)
    lessons_in_week: int = Field(gt=0, lt=8)
    lesson_duration_hours: Decimal = Field(lt=12)
    lesson_type: LessonTypeEnum
    lesson_place: LessonPlaceEnum
    lesson_language: LessonLanguageEnum
    lesson_audience: LessonAudienceEnum
    description: str
    location: LocationInputSchema


class AnnouncementShortOutputSchema(BaseModel):
    id: int
    name: str
    slug: str
    user_id: int
    user_info: dict
    price: Decimal
    description: str
    number_of_views: int
    location: LocationOutputSchema | None
    is_promoted: bool
    created_at: date

    class Config:
        from_attributes = True
