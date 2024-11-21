import uuid

import orjson
from pydantic import BaseModel

from schemas.mixins import TranslatedBaseModel


class ServiceTranslationSchema(BaseModel):
    name: str
    description: str
    language_code: str

    class Config:
        from_attributes = True
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class ServiceSchema(TranslatedBaseModel):
    id: uuid.UUID
    price: int
    image: str
    translations: list[ServiceTranslationSchema]


    class Config:
        from_attributes = True
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class ServiceOutputSchema(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    price: int
    image: str
