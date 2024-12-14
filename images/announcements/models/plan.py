import uuid


from sqlalchemy import BigInteger, Column, ForeignKey, Numeric, String, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.postgres import Base
from models.core import TimeStampedModel
from schemas.plan import PlanAudienceEnum, PlanTypeEnum


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
    discount_price = Column(Numeric(14,2), nullable=True)
    service_type = Column(String(12), nullable=False)
    service_audience = Column(String(20), nullable=False)
    duration=Column(Numeric, nullable=False, default=0)
    is_discount = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
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
