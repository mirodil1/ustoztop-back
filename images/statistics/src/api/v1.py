from fastapi import APIRouter, Depends, Header, HTTPException

from src.services import AnnouncementViewsService

router = APIRouter(
    tags=["statistics"],
    responses={404: {"description": "Not found"}},
)

@router.route("/phone_views/<int:announcement_id>")
async def create_announcement_views(announcement_id: int):
    result = AnnouncementViewsService.create_announcement_views(announcement_id)
    print(result)
    return result
