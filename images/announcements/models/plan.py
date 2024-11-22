import uuid


from sqlalchemy import BigInteger, Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.postgres import Base
from models.core import TimeStampedModel


class Plan(TimeStampedModel):
    __tablename__ = "services"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
    )
    image = Column(String(100))
    price = Column(Numeric(14, 2), nullable=False)

    translations = relationship("PlanTranslation", back_populates="plan")


class PlanTranslation(Base):
    __tablename__ = "services_translation"

    id = Column(BigInteger, primary_key=True)
    language_code = Column(String(length=15))
    name = Column(String(length=255))
    description = Column(String(255))
    master_id = Column(UUID(as_uuid=True), ForeignKey("services.id"))

    plan = relationship("Plan", back_populates="translations")

    def __repr__(self):
        return f"<PlanTranslation(id={self.id}, name='{self.name}')>"
