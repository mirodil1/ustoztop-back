import uuid

from sqlalchemy import BigInteger, Column, ForeignKey, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import Base
from models.core import TimeStampedModel


class Service(TimeStampedModel):
    __tablename__ = "services"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
    )
    image = Column(String(100))
    price = Column(Numeric(14, 2), nullable=False)

    translations = relationship("ServiceTranslation", back_populates="service")


class ServiceTranslation(Base):
    __tablename__ = "services_translation"

    id = Column(BigInteger, primary_key=True)
    language_code = Column(String(length=15))
    name = Column(String(length=255))
    description = Column(String(255))
    master_id = Column(UUID(as_uuid=True), ForeignKey("services.id"))

    service = relationship("Service", back_populates="translations")

    def __repr__(self):
        return f"<ServiceTranslation(id={self.id}, name='{self.name}')>"
