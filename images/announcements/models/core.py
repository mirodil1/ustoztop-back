from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, ARRAY, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from db.postgres import Base


class TimeStampedModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False,
    )


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    uz = Column(String(length=255), nullable=False)
    ru = Column(String(length=255), nullable=False)
    coords = Column(ARRAY(Float), nullable=False)
    parent_id = Column(Integer, ForeignKey("regions.id"), nullable=True)

    parent = relationship(
        "Region",
        backref="children",
        remote_side=[id],
    )
    location = relationship(
        "Location",
        back_populates="region",
    )
