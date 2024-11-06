from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi_filter import FilterDepends
from starlette import status
from starlette.requests import Request

from schemas.announcement import (
    AnnouncementInputSchema,
    AnnouncementOutputSchema,
    AnnouncementStatusEnum,
    AnnouncementShortOutputSchema
)
from schemas.pagination import PaginatedPerPageResponse
from services.announcement import AnnouncementService, get_announcement_service
from services.announcement_filter import AnnouncementFilter


router = APIRouter(
    tags=["announcements"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=PaginatedPerPageResponse[AnnouncementShortOutputSchema])
async def announcements_list(
    announcement_service: AnnouncementService = Depends(get_announcement_service),
    announcement_filter: AnnouncementFilter = FilterDepends(AnnouncementFilter),
    page: int = Query(1, ge=1),
    per_page: int = Query(100, ge=0),
) -> list[AnnouncementShortOutputSchema]:
    paginated_result = await announcement_service.get_announcements(
        announcement_filter,
        page,
        per_page,
    )

    announcement_list = [
        AnnouncementShortOutputSchema(
            id=announcement.id,
            name=announcement.name,
            slug=announcement.slug,
            user_id=announcement.user_id,
            phone_number=announcement.phone_number,
            price=announcement.price,
            location=announcement.location if announcement.location else None,
            description=announcement.description,
            created_at=announcement.created_at.date(),
        ) for announcement in paginated_result["announcements"]
    ]
    return {
        "count": paginated_result["count"],
        "next_page": paginated_result["next_page"],
        "previous_page": paginated_result["previous_page"],
        "items": announcement_list,
    }

@router.get(
    "/user-announcement/",
    status_code=200,
    response_model=list[AnnouncementOutputSchema],
)
async def get_user_announcement(
    request: Request,
    annoincement_service: AnnouncementService = Depends(get_announcement_service),
    status: AnnouncementStatusEnum = Query(AnnouncementStatusEnum.active),
):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401, detail="Not authorized")
    announcements = await annoincement_service.get_user_announcement(
        user_id=request.user.user_id,
        status=status,
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
            location={
                "name": announcement.location.name,
                "coords": [
                    announcement.location.latitude,
                    announcement.location.longitude,
                ],
            },
            is_promoted=announcement.is_promoted,
            promotion_started=announcement.promotion_started,
            promotion_expired=announcement.promotion_expired,
        ) for announcement in announcements
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
            location=announcement.location if announcement.location else None,
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
