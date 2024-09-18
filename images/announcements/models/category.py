from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from announcements.models.core import TimeStampedModel
from announcements.db.postgres import Base


class Category(TimeStampedModel):
    __tablename__ = "category"

    id = Column(BigInteger, primary_key=True)
    icon = Column(String(100))
    order = Column(Integer)
    lft = Column(Integer)
    rght = Column(Integer)
    tree_id = Column(Integer)
    level = Column(Integer)
    parent_id = Column(BigInteger, ForeignKey("category.id"))

    parent = relationship("Category", remote_side=[id], backref="children")
    translations = relationship("CategoryTranslation", back_populates="category")

    project = relationship("Project", back_populates="category")
    blog = relationship("Blog", back_populates="category")


class CategoryTranslation(Base):
    __tablename__ = "category_translation"

    id = Column(BigInteger, primary_key=True)
    language_code = Column(String(15))
    name = Column(String(255))
    slug = Column(String(255))
    master_id = Column(BigInteger, ForeignKey("category.id"))

    category = relationship("Category", back_populates="translations")

    def __repr__(self):
        return f"<CategoryTranslation(id={self.id}, name='{self.name}')>"
