from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.postgres import Base
from models.core import TimeStampedModel


class Category(TimeStampedModel):
    __tablename__ = "category"

    id = Column(BigInteger, primary_key=True)
    icon = Column(String(length=100))
    order = Column(Integer)
    lft = Column(Integer)
    rght = Column(Integer)
    tree_id = Column(Integer)
    level = Column(Integer)
    parent_id = Column(BigInteger, ForeignKey("category.id"))

    parent = relationship("Category", remote_side=[id], backref="children")
    translations = relationship("CategoryTranslation", back_populates="category")


class CategoryTranslation(Base):
    __tablename__ = "category_translation"

    id = Column(BigInteger, primary_key=True)
    language_code = Column(String(length=15))
    name = Column(String(length=255))
    slug = Column(String(length=255), unique=True)
    master_id = Column(BigInteger, ForeignKey("category.id"))

    category = relationship("Category", back_populates="translations")

    def __repr__(self):
        return f"<CategoryTranslation(id={self.id}, name='{self.name}')>"
