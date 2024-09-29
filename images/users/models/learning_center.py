from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Time,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from models.core import TimeStampedModel
from db.postgres import Base
from schemas.learning_center import DayOfWeek


class LearningCenter(TimeStampedModel):
    __tablename__ = "learning_center"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=255), nullable=False)
    description = Column(String, nullable=True)

    user_id = Column(BigInteger, ForeignKey("users.id"))
    user = relationship("User", back_populates="learning_center", single_parent=True)

    branch = relationship("Branch", back_populates="learning_center")
    working_schedule = relationship("WorkingSchedule", back_populates="learning_center")

    __table_args__ = (UniqueConstraint("user_id"),)


class Branch(Base):
    __tablename__ = "branch"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=255), nullable=False)

    learning_center_id = Column(BigInteger, ForeignKey("learning_center.id"))
    learning_center = relationship("LearningCenter", back_populates="branch")


class WorkingSchedule(Base):
    __tablename__ = "working_schedule"

    id = Column(BigInteger, primary_key=True)
    day_of_week = Column(Enum(DayOfWeek), nullable=False)
    opening_time = Column(Time, nullable=True)
    closing_time = Column(Time, nullable=True)
    is_closed = Column(Boolean, default=False)

    learning_center_id = Column(BigInteger, ForeignKey("learning_center.id"))
    learning_center = relationship("LearningCenter", back_populates="working_schedule")

    __table_args__ = (UniqueConstraint(
        "learning_center_id",
        "day_of_week",
        name='uix_learning_center_id_day_of_week'),
    )
