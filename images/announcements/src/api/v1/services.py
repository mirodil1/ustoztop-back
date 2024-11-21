from core.config import settings
from fastapi import APIRouter, Depends, Header, HTTPException, Query
from schemas.pagination import PaginatedPerPageResponse
from schemas.service import ServiceOutputSchema
from services.service import ServicesService, get_service
from starlette import status

router = APIRouter(
    tags=["services"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[ServiceOutputSchema])
async def services_list(
    service: ServicesService = Depends(get_service),
    X_language: str = Header(...),
):
    if X_language not in settings.languages["available"]:
        X_language = settings.languages["default"]

    services = await service.get_services(X_language)
    services_list = [
            ServiceOutputSchema(
                id=service.get("id"),
                name=service.get("name"),
                description=service.get("description"),
                price=service.get("price"),
                image=f"{settings.base_url}/media/{service.get('image')}" \
                    if service.get("image") else None,
                children=service.get("children"),
            ) for service in services
        ]
    return services_list


# @router.get("/{category_id}", response_model=ServiceOutputSchema)
# async def category_detail(
#     category_id: int,
#     category_service: ServiceOutputSchema = Depends(get_service),
#     X_language: str = Header(...),
# ):
#     if X_language not in settings.languages["available"]:
#         X_language = settings.languages["default"]

#     category = await category_service.get_category_by_id(
#         category_id=category_id,
#         language=X_language,
#     )
#     if not category:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Not found",
#         )
#     return ServiceOutputSchema(
#                 id=category.get("id"),
#                 name=category.get("name"),
#                 description=category.get("description"),
#                 order=category.get("order"),
#                 icon=f"{settings.base_url}/media/{category.get('icon')}" \
#                     if category.get("icon") else None,
#                 children=category.get("children"),
#             )
