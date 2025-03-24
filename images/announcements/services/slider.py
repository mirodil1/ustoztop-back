import uuid
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session, joinedload

from db.postgres import get_db
from models.slider import Slider
from schemas.slider import SliderSchema


class SliderService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_sliders(self, language: str):
        sliders = (
            self.db.query(Slider)
                .options(
                    joinedload(Slider.translations),
                ).filter(Slider.is_active==True)
                .order_by(
                    Slider.slider_order.desc(),
                )
        )
        translated = [
            SliderSchema.model_validate(slider).model_dump(language=language)
            for slider in sliders
        ]
        return translated

@lru_cache
def get_slider(db: Session = Depends(get_db)) -> SliderService:
    return SliderService(db)
