from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from models.core import TimeStampedModel
from db.postgres import Base


class Slider(TimeStampedModel):
    __tablename__ = "sliders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=False)
    slider_order = Column(Integer, default=0)

    translations = relationship("SliderTranslation", back_populates="slider", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Slider(name={self.name}, is_active={self.is_active}, slider_order={self.slider_order})>"


class SliderTranslation(Base):
    __tablename__ = 'sliders_translation'

    id = Column(Integer, primary_key=True)
    language_code = Column(String(length=15))
    image_large = Column(String)
    image_medium = Column(String)
    link = Column(String(500))
    master_id = Column(Integer, ForeignKey("sliders.id"))

    slider = relationship("Slider", back_populates="translations")
