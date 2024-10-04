from sqlalchemy import (UniqueConstraint)
from sqlalchemy.orm import relationship

from src.models.core import TimeStampedModel
from src.db import db
from src.schemas.learning_center import DayOfWeek


class LearningCenter(TimeStampedModel):
    __tablename__ = "learning_center"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=255), nullable=True)
    description = db.Column(db.String, nullable=True)

    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="learning_center", single_parent=True)

    branch = relationship("Branch", back_populates="learning_center")
    working_schedule = relationship("WorkingSchedule", back_populates="learning_center")

    __table_args__ = (UniqueConstraint("user_id"),)


class Branch(db.Model):
    __tablename__ = "branch"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=255), nullable=False)

    learning_center_id = db.Column(db.BigInteger, db.ForeignKey("learning_center.id"))
    learning_center = relationship("LearningCenter", back_populates="branch")


class WorkingSchedule(db.Model):
    __tablename__ = "working_schedule"

    id = db.Column(db.BigInteger, primary_key=True)
    day_of_week = db.Column(db.Enum(DayOfWeek), nullable=False)
    opening_time = db.Column(db.Time, nullable=True)
    closing_time = db.Column(db.Time, nullable=True)
    is_closed = db.Column(db.Boolean, default=False)

    learning_center_id = db.Column(db.BigInteger, db.ForeignKey("learning_center.id"))
    learning_center = relationship("LearningCenter", back_populates="working_schedule")

    __table_args__ = (UniqueConstraint(
        "learning_center_id",
        "day_of_week",
        name='uix_learning_center_id_day_of_week'),
    )
