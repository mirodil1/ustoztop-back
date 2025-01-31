from functools import lru_cache

from db.postgres import get_db
from fastapi import Depends
from models.core import Region
from schemas.core import RegionOutputSchema
from sqlalchemy.orm import Session, joinedload


class RegionService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_regions(self):
        categories = (
            self.db.query(Region)
                .options(
                    joinedload(Region.parent),
                )
                .filter(Region.parent_id.is_(None))
        )

        return categories

    async def get_cities(
            self,
            region_id: int,
    ) -> RegionOutputSchema | None:
        regions = self.db.query(Region).filter(Region.parent_id == region_id).all()
        if regions:
            return regions
        return None

    async def get_districts(
            self,
            region_id: int,
    ) -> RegionOutputSchema | None:
        regions = self.db.query(Region).filter(Region.parent_id == region_id).all()
        if regions:
            return regions
        return None

@lru_cache
def get_region_service(db: Session = Depends(get_db)) -> RegionService:
    return RegionService(db)
