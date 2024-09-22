from sqlalchemy import (BigInteger, Boolean, Column, Date, Enum, ForeignKey,
                        Integer, Numeric, String)
from sqlalchemy.orm import relationship

from models.core import TimeStampedModel
from schemas.announcement import (LessonAudienceEnum, LessonLanguageEnum,
                                  LessonPlaceEnum, LessonTypeEnum)


class Announcement(TimeStampedModel):
    __tablename__ = "announcement"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=255), nullable=False)
    slug = Column(String(length=255), unique=True, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    phone_number = Column(String(length=14), nullable=False)
    price = Column(Numeric(14, 2), nullable=False)
    lessons_in_week = Column(Integer, nullable=False) 
    lesson_duration_hours = Column(Integer, nullable=False)
    lesson_type = Column(Enum(LessonTypeEnum), nullable=False)
    lesson_place = Column(Enum(LessonPlaceEnum), nullable=False)
    lesson_language = Column(Enum(LessonLanguageEnum), nullable=False)
    lesson_audience = Column(Enum(LessonAudienceEnum), nullable=True)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_confirmed_by_admin = Column(Boolean, default=False)
    is_promoted = Column(Boolean, default=False)
    promotion_started = Column(Date, nullable=True)
    promotion_expired = Column(Date, nullable=True)

    category_id = Column(BigInteger, ForeignKey("category.id"), nullable=False)
    category = relationship("Category", back_populates="announcement")
 