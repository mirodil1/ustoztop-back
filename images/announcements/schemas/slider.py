from pydantic import BaseModel

from schemas.mixins import TranslatedBaseModel


class SliderTranslationSchema(BaseModel):
    link: str
    image_large: str
    image_medium: str
    language_code: str
    
    class Config:
        from_attributes = True


class SliderSchema(TranslatedBaseModel):
    id: int
    name: str
    slider_order: int
    translations: list[SliderTranslationSchema]

    class Config:
        from_attributes = True


class SliderOutputSchema(BaseModel):
    id: int
    name: str
    link: str
    image_large: str
    image_medium: str
    slider_order: int
