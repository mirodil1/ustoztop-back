from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.models import AnnouncementViews, ProfileViews, PhoneNumberViews
from src.services import (
    AccountViewsService,
    AnnouncementViewsService,
    PhoneNumberViewsService,
    get_account_stat_service,
    get_announcement_stat_service,
    get_phone_number_stat_service,
)

router = APIRouter(
    tags=["statistics"],
    responses={404: {"description": "Not found"}},
)


@router.post("/announcement_views/create/{announcement_id}", include_in_schema=False)
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
    "/announcement_veiws_count/{announcement_id}",
    include_in_schema=False,
)
async def get_announcement_veiws_count_by_id(
    announcement_id: int,
    announc_statistic_service: AnnouncementViewsService = Depends(
        get_announcement_stat_service),
):
    result = await announc_statistic_service.get_views_count_by_id(announcement_id)
    return result


@router.get(
    "/announcement_views/{announcement_id}",
    response_model=list[AnnouncementViews],
)
async def get_announcement_views(
    request: Request,
    announcement_id: int,
    announc_statistic_service: AnnouncementViewsService = Depends(
        get_announcement_stat_service),
):
    if not request.user:
        raise HTTPException(status_code=401, detail="Not authorized")
    result = await announc_statistic_service.get_last_views(announcement_id)

    return result


@router.post("/account_views/create/{user_id}", include_in_schema=False)
async def create_account_views(
    user_id: int,
    request: Request,
    account_statistic_service: AccountViewsService = Depends(
        get_account_stat_service),
):
    data = request.headers.get("user-agent")
    result = await account_statistic_service.create_account_views(
        user_id,
        data,
    )
    if result is None or result.inserted_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create account view.",
        )
    return str(result.inserted_id)


@router.get(
    "/account_views",
    response_model=list[ProfileViews],
)
async def get_account_views(
    request: Request,
    account_statistic_service: AccountViewsService = Depends(
        get_account_stat_service),
):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401, detail="Not authorized")
    result = await account_statistic_service.get_account_views(request.user.user_id)
    return result


@router.post("/phone_number_views/create/{announcement_id}", include_in_schema=False)
async def create_phone_number_views(
    announcement_id: int,
    request: Request,
    phone_number_statistic_service: PhoneNumberViewsService = Depends(
        get_phone_number_stat_service),
):
    data = request.headers.get("user-agent")
    result = await phone_number_statistic_service.create_phone_number_views(
        announcement_id,
        data,
    )
    if result is None or result.inserted_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create phone number view.",
        )
    return str(result.inserted_id)


@router.get(
    "/phone_number_views/get/{announcement_id}",
    response_model=PhoneNumberViews,
    include_in_schema=False
)
async def get_phone_number_views(
    request: Request,
    announcement_id: int,
    phone_number_statistic_service: PhoneNumberViewsService = Depends(
        get_phone_number_stat_service),
):
    result = await phone_number_statistic_service.get_phone_number_count(announcement_id)
    return result
