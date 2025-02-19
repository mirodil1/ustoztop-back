import enum

from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi_filter import FilterDepends, with_prefix

from models.announcement import (
    Announcement,
    Location,
    LessonAudienceEnum,
    LessonLanguageEnum,
    LessonPlaceEnum,
    LessonTypeEnum,
)

class OrderEnum(enum.Enum):
    CREATED_AT_ASC = "created_at"
    CREATED_AT_DESC = "-created_at"
    PRICE_ASC = "price"
    PRICE_DESC = "-price"


class LocationFilter(Filter):
    region_id: int | None = None

    class Constants(Filter.Constants):
        model = Location


class AnnouncementFilter(Filter):
    id__in: list | None = None
    search: str | None = None
    ordering: OrderEnum = OrderEnum.CREATED_AT_DESC
    price__gte: int | None = None
    price__lte: int | None = None
    lesson_type: LessonTypeEnum | None = None
    lesson_language: LessonLanguageEnum | None = None
    lesson_audience: LessonAudienceEnum | None = None
    lesson_place: LessonPlaceEnum | None = None
    category_id: int | None = None
    gender: str | None = None
    role: str | None = None
    region: LocationFilter | None = FilterDepends(with_prefix("location", LocationFilter))

    class Constants(Filter.Constants):
        model = Announcement
        search_field_name = "search"
        search_model_fields = ["name", "description"]
