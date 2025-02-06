import enum
import uuid

import orjson
from pydantic import BaseModel

from schemas.mixins import TranslatedBaseModel


class PlanAudienceEnum(enum.Enum):
    all = "all"
    tutor = "tutor"
    learning_center = "learning_center"


class PlanTypeEnum(enum.Enum):
    top = "top"
    premium = "premuim"


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
    discount_price: int
    service_type: str
    service_audience: str
    duration: int
    is_discount: bool
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
    discount_price: int
    plan_type: str
    plan_audience: str
    duration: int
    is_discount: bool
    image: str


class PlanOutputShortSchema(BaseModel):
    id: uuid.UUID
    price: int
    plan_type: str
    plan_audience: str
    duration: int
