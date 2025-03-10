from fastapi import APIRouter, Depends, Header, HTTPException, Query

from starlette import status

from core.config import settings
from schemas.category import CategoryOutputSchema
from schemas.pagination import PaginatedPerPageResponse
from services.category import CategoryService, get_category_service


router = APIRouter(
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=PaginatedPerPageResponse[CategoryOutputSchema])
async def categories_list(
    category_service: CategoryService = Depends(get_category_service),
    X_language: str = Header(...),
    page: int = Query(1, ge=1),
    per_page: int = Query(100, ge=0),
):

    if X_language not in settings.languages["available"]:
        X_language = settings.languages["default"]

    paginated_result = await category_service.get_categories(X_language, page, per_page)
    categories = [
            CategoryOutputSchema(
                id=category.get("id"),
                name=category.get("name"),
                slug=category.get("slug"),
                order=category.get("order"),
                icon=f"{settings.base_url}/media/{category.get('icon')}" \
                    if category.get("icon") else None,
                announcement_count=category.get("announcement_count", 0),    
                children=category.get("children"),
            ) for category in paginated_result["categories"]
        ]
    return {
        "count": paginated_result["count"],
        "next_page": paginated_result["next_page"],
        "previous_page": paginated_result["previous_page"],
        "items": categories,
    }


@router.get("/{category_id}", response_model=CategoryOutputSchema)
async def category_detail(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
    X_language: str = Header(...),
):
    if X_language not in settings.languages["available"]:
        X_language = settings.languages["default"]

    category = await category_service.get_category_by_id(
        category_id=category_id,
        language=X_language,
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )
    return CategoryOutputSchema(
                id=category.get("id"),
                name=category.get("name"),
                slug=category.get("slug"),
                order=category.get("order"),
                icon=f"{settings.base_url}/media/{category.get('icon')}" \
                    if category.get("icon") else None,
                children=category.get("children"),
            )
