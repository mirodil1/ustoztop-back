import uuid

from starlette import status
from fastapi import APIRouter, Depends, Header, HTTPException

from core.config import settings
from schemas.plan import PlanOutputSchema, PlanOutputShortSchema
from services.plan import PlanService, get_service

router = APIRouter(
    tags=["services"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[PlanOutputSchema])
async def services_list(
    plan_service: PlanService = Depends(get_service),
    X_language: str = Header(...),
):
    if X_language not in settings.languages["available"]:
        X_language = settings.languages["default"]

    services = await plan_service.get_plans(X_language)
    services_list = [
            PlanOutputSchema(
                id=plan.get("id"),
                name=plan.get("name"),
                description=plan.get("description"),
                price=plan.get("price"),
                discount_price=plan.get("discount_price"),
                plan_type=plan.get("service_type"),
                plan_audience=plan.get("service_audience"),
                duration=plan.get("duration"),
                is_discount=plan.get("is_discount"),
                image=f"{settings.base_url}/media/{plan.get('image')}" \
                    if plan.get("image") else None,
                children=plan.get("children"),
            ) for plan in services
        ]
    return services_list


@router.get("/{plan_id}")
async def service_detail(
    plan_id: uuid.UUID,
    plan_service: PlanService = Depends(get_service),
):
    plan = await plan_service.get_plan_by_id(plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )
    return PlanOutputShortSchema(
        id=plan.id,
        price=plan.price,
        plan_type=plan.service_type,
        plan_audience=plan.service_audience,
        duration=plan.duration,
        discount_price=plan.discount_price,
        is_discount=plan.is_discount,
    )
