from functools import lru_cache

from db.postgres import get_db
from fastapi import Depends
from models.service import Service
from schemas.service import ServiceSchema
from sqlalchemy.orm import Session, joinedload


class ServicesService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_services(self, language: str):
        services = (
            self.db.query(Service)
                .options(
                    joinedload(Service.translations),
                ).all()
        )
        translated = [
            ServiceSchema.model_validate(service).model_dump(language=language)
            for service in services
        ]
        return translated

    async def get_service_by_id(
            self,
            service_id: int,
            language: str,
    ) -> ServiceSchema | None:
        service = self.db.query(Service).filter(Service.id==service_id).scalar()
        if service:
            return ServiceSchema.model_validate(Service).model_dump(language=language)
        return None

@lru_cache
def get_service(db: Session = Depends(get_db)) -> ServicesService:
    return ServicesService(db)
