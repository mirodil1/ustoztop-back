import orjson
from pydantic import BaseModel


class RegionOutputSchema(BaseModel):
    id: int
    uz: str
    ru: str
    coords: list
