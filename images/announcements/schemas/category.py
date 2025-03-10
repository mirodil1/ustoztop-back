import orjson
from pydantic import BaseModel

from schemas.mixins import TranslatedBaseModel


class CategoryTranslationSchema(BaseModel):
    name: str
    slug: str
    language_code: str

    class Config:
        from_attributes = True
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class CategorySchema(TranslatedBaseModel):
    id: int
    order: int
    icon: str
    announcement_count: int = 0
    translations: list[CategoryTranslationSchema]
    children: list["CategorySchema"]

    class Config:
        from_attributes = True
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class CategoryOutputSchema(BaseModel):
    id: int
    name: str
    slug: str
    order: int
    icon: str | None
    announcement_count: int = 0
    children: list["CategoryOutputSchema"] = []
