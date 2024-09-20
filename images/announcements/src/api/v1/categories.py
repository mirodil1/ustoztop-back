from fastapi import APIRouter, Depends, Header, Request
from starlette import status
from starlette.responses import RedirectResponse

from core.config import LANGUAGES
from services.category import CategoryService, get_category_service

router = APIRouter(
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_categories(
    category_service: CategoryService = Depends(get_category_service),
    X_language: str = Header(...)
):
    if X_language not in LANGUAGES["available"]:
        X_language = LANGUAGES["default"]
        
    categories = await category_service.get_categories(X_language)
    return categories
