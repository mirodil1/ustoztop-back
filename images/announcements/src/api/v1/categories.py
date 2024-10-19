from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException
from starlette import status
from starlette.responses import RedirectResponse

from core.config import settings
from schemas.category import CategoryOutputSchema
from services.category import CategoryService, get_category_service

router = APIRouter(
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[CategoryOutputSchema])
async def categories_list(
    category_service: CategoryService = Depends(get_category_service),
    X_language: str = Header(...)
):
    if X_language not in settings.languages["available"]:
        X_language = settings.languages["default"]
        
    categories = await category_service.get_categories(X_language)
    return [
            CategoryOutputSchema(
                id=category.get("id"),
                name=category.get("name"),
                slug=category.get("slug"),
                order=category.get("order"),
                icon=category.get("icon"),
                children=category.get("children")
            ) for category in categories
        ]


@router.get("/{category_id}", response_model=CategoryOutputSchema)
async def category_detail(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
    X_language: str = Header(...)
):
    if X_language not in settings.languages["available"]:
        X_language = settings.languages["default"]
        
    category = await category_service.get_category_by_id(
        category_id=category_id,
        language=X_language
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    return CategoryOutputSchema(
                id=category.get("id"),
                name=category.get("name"),
                slug=category.get("slug"),
                order=category.get("order"),
                icon=category.get("icon"),
                children=category.get("children")
            )