import uuid

import orjson
from pydantic import BaseModel

from schemas.mixins import TranslatedBaseModel


class PlanTranslationSchema(BaseModel):
    name: str
    description: str
    language_code: str

    class Config:
        from_attributes = True
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class PlanSchema(TranslatedBaseModel):
    id: uuid.UUID
    price: int
    image: str
    translations: list[PlanTranslationSchema]


    class Config:
        from_attributes = True
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class PlanOutputSchema(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    price: int
    image: str


class PlanOutputShortSchema(BaseModel):
    id: uuid.UUID
    price: int
