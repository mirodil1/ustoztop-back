from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from schemas.announcement import AnnouncementInputSchema, AnnouncementOutputSchema
from services.announcement import AnnouncementService, get_announcement_service
from starlette import status
from starlette.requests import Request

router = APIRouter(
    tags=["announcements"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[AnnouncementOutputSchema])
async def announcements_list(
    announcement_service: AnnouncementService = Depends(get_announcement_service),
) -> list[AnnouncementOutputSchema]:
    announcements_list = await announcement_service.get_announcements()

    filtered_list = [
        AnnouncementOutputSchema(
            id=announcement.id,
            name=announcement.name,
            slug=announcement.slug,
            user_id=announcement.user_id,
            category_id= announcement.category_id,
            phone_number=announcement.phone_number,
            price=announcement.price,
            lessons_in_week=announcement.lessons_in_week,
            lesson_duration_hours= announcement.lesson_duration_hours,
            lesson_type= announcement.lesson_type,
            lesson_place= announcement.lesson_place,
            lesson_language=announcement.lesson_language,
            lesson_audience=announcement.lesson_audience,
            description=announcement.description,
            is_promoted=announcement.is_promoted,
            promotion_started=announcement.promotion_started,
            promotion_expired=announcement.promotion_expired,
        ) for announcement in announcements_list
    ]
    return filtered_list


@router.get("/{slug}/", response_model=AnnouncementOutputSchema)
async def announcements_detail(
    request: Request,
    slug: str,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
) -> AnnouncementOutputSchema:
    user_agent = request.headers.get("user-agent", "unknown")
    announcement = await announcement_service.get_announcement_by_slug(slug=slug, user_agent=user_agent)

    if not announcement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )
    
    return AnnouncementOutputSchema(
            id=announcement.id,
            name=announcement.name,
            slug=announcement.slug,
            user_id=announcement.user_id,
            category_id= announcement.category_id,
            phone_number=announcement.phone_number,
            price=announcement.price,
            lessons_in_week=announcement.lessons_in_week,
            lesson_duration_hours= announcement.lesson_duration_hours,
            lesson_type= announcement.lesson_type,
            lesson_place= announcement.lesson_place,
            lesson_language=announcement.lesson_language,
            lesson_audience=announcement.lesson_audience,
            description=announcement.description,
            is_promoted=announcement.is_promoted,
            promotion_started=announcement.promotion_started,
            promotion_expired=announcement.promotion_expired,
        )


@router.get("/category/{category_id}/", response_model=list[AnnouncementOutputSchema])
async def announcements_by_category(
    category_id: int,
    announcement_service: AnnouncementService = Depends(get_announcement_service),
) -> list[AnnouncementOutputSchema]:
    announcements = await announcement_service.get_announcement_by_category(
        category_id=category_id,
    )

    filtered_list = [
        AnnouncementOutputSchema(
            id=announcement.id,
            name=announcement.name,
            slug=announcement.slug,
            user_id=announcement.user_id,
            category_id= announcement.category_id,
            phone_number=announcement.phone_number,
            price=announcement.price,
            lessons_in_week=announcement.lessons_in_week,
            lesson_duration_hours= announcement.lesson_duration_hours,
            lesson_type= announcement.lesson_type,
            lesson_place= announcement.lesson_place,
            lesson_language=announcement.lesson_language,
            lesson_audience=announcement.lesson_audience,
            description=announcement.description,
            is_promoted=announcement.is_promoted,
            promotion_started=announcement.promotion_started,
            promotion_expired=announcement.promotion_expired,
        ) for announcement in announcements
    ]
    return filtered_list


@router.post("/announcement/create/", status_code=201)
async def create_new_announcement(
    request: Request,
    announcement: AnnouncementInputSchema,
    annoincement_service: AnnouncementService = Depends(get_announcement_service),
):
    if not request.user:
        raise HTTPException(status_code=401, detail="Not authorized")
    announcement_data = announcement.dict()
    announcement = await annoincement_service.create_announcement(
        user_id=request.user.user_id,
        data=announcement_data,
    )
    if announcement:
        return {"message": "created"}
    raise HTTPException(
        status_code=400, detail="Something went wrong, please try again"
    )
