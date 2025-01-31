from fastapi import APIRouter, Depends, Header, HTTPException, Query

from starlette import status

from core.config import settings
from schemas.core import RegionOutputSchema
from services.core import RegionService, get_region_service


router = APIRouter(
    tags=["regions"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[RegionOutputSchema])
async def regions_list(
    region_service: RegionService = Depends(get_region_service),
):
    result = await region_service.get_regions()
    return result


@router.get("/{region_id}/cities/", response_model=list[RegionOutputSchema])
async def cities_list(
    region_id: int,
    region_service: RegionService = Depends(get_region_service)):

    region = await region_service.get_cities(region_id)
    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )
    return region


@router.get("/{city_id}/districts/", response_model=list[RegionOutputSchema])
async def districts_list(
    city_id: int,
    region_service: RegionService = Depends(get_region_service)):

    districts = await region_service.get_districts(city_id)
    if not districts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )
    return districts
