from fastapi import APIRouter, Depends, Header, HTTPException

from src.services import AnnouncementViewsService, get_announcement_stat_service
import json
from bson import json_util

router = APIRouter(
    tags=["statistics"],
    responses={404: {"description": "Not found"}},
)

@router.post("/phone_views/<int:announcement_id>")
async def create_announcement_views(
    announcement_id: int,
    announc_statistic_service: AnnouncementViewsService = Depends(get_announcement_stat_service)
):
    result = await announc_statistic_service.create_announcement_views(announcement_id)
    print(result)
    return str(result.inserted_id)


@router.get("/phone_views/<int:announcement_id>")
async def create_announcement_views(
    announcement_id: int,
    announc_statistic_service: AnnouncementViewsService = Depends(get_announcement_stat_service)
):
    result = await announc_statistic_service.get_announcement_views(announcement_id)

    print(result)
    return {"result":json.loads(json_util.dumps(result))}
