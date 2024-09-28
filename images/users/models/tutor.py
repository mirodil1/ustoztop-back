from db.postgres import Base
from schemas.tutor import EducationDegree, LanguageLevel
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from models.core import TimeStampedModel


class Tutor(TimeStampedModel):
    __tablename__ = "tutor"

    id = Column(BigInteger, primary_key=True)
    first_name = Column(String(length=64), nullable=False)
    last_name = Column(String(length=64), nullable=False)
    gender = Column(String(length=6), nullable=False)
    
    user_id = Column(BigInteger, ForeignKey("users.id"))
    user = relationship("User", back_populates="tutor", single_parent=True)

    language = relationship("Language", back_populates="tutor")
    education = relationship("Education", back_populates="tutor")
    experience = relationship("Experience", back_populates="tutor")

    __table_args__ = (UniqueConstraint("user_id"),)


class Language(Base):
    __tablename__ = "language"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=64), nullable=False)
    level = Column(Enum(LanguageLevel), nullable=False)

    tutor_id = Column(BigInteger, ForeignKey("tutor.id"))
    tutor = relationship("Tutor", back_populates="language")


class Education(Base):
    __tablename__ = "education"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=255), nullable=False)
    degree = Column(Enum(EducationDegree), nullable=False)
    field_of_study = Column(String(length=255), nullable=False)
    start_year = Column(Date, nullable=True)
    finish_year = Column(Date, nullable=True)

    tutor_id = Column(BigInteger, ForeignKey("tutor.id"))
    tutor = relationship("Tutor", back_populates="education")


class Experience(Base):
    __tablename__ = "experience"

    id = Column(BigInteger, primary_key=True)
    organization = Column(String(length=255), nullable=False)
    position = Column(String(length=255), nullable=False)
    start_year = Column(Date, nullable=False)
    finish_year = Column(Date, nullable=True)
    is_working = Column(Boolean, default=False)

    tutor_id = Column(BigInteger, ForeignKey("tutor.id"))
    tutor = relationship("Tutor", back_populates="experience")
