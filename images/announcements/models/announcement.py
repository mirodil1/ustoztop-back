import uuid

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.postgres import Base
from schemas.announcement import (
    AnnouncementStatusEnum,
    LessonAudienceEnum,
    LessonLanguageEnum,
    LessonPlaceEnum,
    LessonTypeEnum,
)
from models.core import TimeStampedModel


class Location(Base):
    __tablename__ = "locations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    uz = Column(String(length=255), nullable=False)
    ru = Column(String(length=255), nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)

    announcement = relationship(
        "Announcement", uselist=False, back_populates="location",
    )


class Announcement(TimeStampedModel):
    __tablename__ = "announcement"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=255), nullable=False)
    slug = Column(String(length=255), unique=True, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    phone_number = Column(String(length=14), nullable=False)
    price = Column(Numeric(14, 2), nullable=False)
    lessons_in_week = Column(Integer, nullable=True)
    lesson_duration_hours = Column(Numeric(2, 1), nullable=False)
    lesson_type = Column(Enum(LessonTypeEnum), nullable=False)
    lesson_place = Column(Enum(LessonPlaceEnum), nullable=False)
    lesson_language = Column(Enum(LessonLanguageEnum), nullable=False)
    lesson_audience = Column(Enum(LessonAudienceEnum), nullable=True)
    description = Column(String, nullable=False)
    status = Column(
        Enum(AnnouncementStatusEnum), default=AnnouncementStatusEnum.waiting,
    )
    is_active = Column(Boolean, default=False)
    is_confirmed_by_admin = Column(Boolean, default=False)
    is_promoted = Column(Boolean, default=False)
    promotion_started = Column(Date, nullable=True)
    promotion_expired = Column(Date, nullable=True)

    category_id = Column(BigInteger, ForeignKey("category.id"), nullable=False)
    category = relationship("Category", back_populates="announcement")

    location_id = Column(UUID, ForeignKey("locations.id"), nullable=False)
    location = relationship("Location", back_populates="announcement")
