from fastapi import APIRouter, Depends, Header

from core.config import settings
from schemas.slider import SliderOutputSchema
from services.slider import SliderService, get_slider

router = APIRouter(
    tags=["sliders"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[SliderOutputSchema])
async def sliders_list(
    slider_service: SliderService = Depends(get_slider),
    X_language: str = Header(...),
):
    if X_language not in settings.languages["available"]:
        X_language = settings.languages["default"]

    sliders = await slider_service.get_sliders(X_language)

    sliders_list = [
            SliderOutputSchema(
                id=slider.get("id"),
                name=slider.get("name"),
                link=slider.get("link"),
                slider_order=slider.get("slider_order"),
                image_large=f"{settings.base_url}/media/{slider.get('image_large')}" \
                    if slider.get("image_large") else None,
                image_medium=f"{settings.base_url}/media/{slider.get('image_medium')}" \
                    if slider.get("image_medium") else None,
            ) for slider in sliders
        ]
    return sliders_list
