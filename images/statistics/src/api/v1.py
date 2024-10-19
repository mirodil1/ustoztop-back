from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.models import AnnouncementViews
from src.services import AnnouncementViewsService, get_announcement_stat_service

router = APIRouter(
    tags=["statistics"],
    responses={404: {"description": "Not found"}},
)


@router.post("/announcement_views/craete/{announcement_id}")
async def create_announcement_views(
    announcement_id: int,
    request: Request,
    announc_statistic_service: AnnouncementViewsService = Depends(
        get_announcement_stat_service),
):
    data = request.headers.get("user-agent")
    result = await announc_statistic_service.create_announcement_views(
        announcement_id,
        data,
    )
    if result is None or result.inserted_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create announcement view.",
        )
    return str(result.inserted_id)


@router.get(
    "/announcement_views/{announcement_id}",
    response_model=list[AnnouncementViews],
)
async def get_announcement_views(
    announcement_id: int,
    announc_statistic_service: AnnouncementViewsService = Depends(
        get_announcement_stat_service),
):
    result = await announc_statistic_service.get_announcement_views(announcement_id)
    return result
