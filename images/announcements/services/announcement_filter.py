from fastapi_filter.contrib.sqlalchemy import Filter
from models.announcement import (
    Announcement,
    LessonAudienceEnum,
    LessonLanguageEnum,
    LessonPlaceEnum,
    LessonTypeEnum,
)


class AnnouncementFilter(Filter):
    price__gte: int | None = None
    price__lte: int | None = None
    lesson_type__in: list[LessonTypeEnum] | None = None
    lesson_language__in: list[LessonLanguageEnum] | None = None
    lesson_audience__in: list[LessonAudienceEnum] | None = None
    lesson_place__in: list[LessonPlaceEnum] | None = None
    category_id: int | None = None

    class Constants(Filter.Constants):
        model = Announcement
