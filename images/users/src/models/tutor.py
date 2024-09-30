from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from src.models.core import TimeStampedModel
from src.db import db
from src.schemas.tutor import EducationDegree, LanguageLevel


class Tutor(TimeStampedModel):
    __tablename__ = "tutor"

    id = db.Column(db.BigInteger, primary_key=True)
    first_name = db.Column(db.String(length=64), nullable=False)
    last_name = db.Column(db.String(length=64), nullable=False)
    gender = db.Column(db.String(length=6), nullable=False)
    
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="tutor", single_parent=True)

    language = relationship("Language", back_populates="tutor")
    education = relationship("Education", back_populates="tutor")
    experience = relationship("Experience", back_populates="tutor")

    __table_args__ = (UniqueConstraint("user_id"),)


class Language(db.Model):
    __tablename__ = "language"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=64), nullable=False)
    level = db.Column(db.Enum(LanguageLevel), nullable=False)

    tutor_id = db.Column(db.BigInteger, db.ForeignKey("tutor.id"))
    tutor = relationship("Tutor", back_populates="language")


class Education(db.Model):
    __tablename__ = "education"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=255), nullable=False)
    degree = db.Column(db.Enum(EducationDegree), nullable=False)
    field_of_study = db.Column(db.String(length=255), nullable=False)
    start_year = db.Column(db.Date, nullable=True)
    finish_year = db.Column(db.Date, nullable=True)

    tutor_id = db.Column(db.BigInteger, db.ForeignKey("tutor.id"))
    tutor = relationship("Tutor", back_populates="education")


class Experience(db.Model):
    __tablename__ = "experience"

    id = db.Column(db.BigInteger, primary_key=True)
    organization = db.Column(db.String(length=255), nullable=False)
    position = db.Column(db.String(length=255), nullable=False)
    start_year = db.Column(db.Date, nullable=False)
    finish_year = db.Column(db.Date, nullable=True)
    is_working = db.Column(db.Boolean, default=False)

    tutor_id = db.Column(db.BigInteger, db.ForeignKey("tutor.id"))
    tutor = relationship("Tutor", back_populates="experience")
