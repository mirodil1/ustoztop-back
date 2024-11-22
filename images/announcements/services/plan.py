import uuid
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session, joinedload

from db.postgres import get_db
from models.plan import Plan
from schemas.plan import PlanSchema


class PlanService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_plans(self, language: str):
        plans = (
            self.db.query(Plan)
                .options(
                    joinedload(Plan.translations),
                ).all()
        )
        translated = [
            PlanSchema.model_validate(plan).model_dump(language=language)
            for plan in plans
        ]
        return translated

    async def get_plan_by_id(self, plan_id: uuid.UUID) -> PlanSchema | None:
        plan = self.db.query(Plan).filter(Plan.id==plan_id).scalar()
        if plan:
            return plan
        return None

@lru_cache
def get_service(db: Session = Depends(get_db)) -> PlanService:
    return PlanService(db)
