from typing import Annotated
from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status


router = APIRouter()


class Announcement(BaseModel):
    id: str
    title: str
    # description: str
    # slug: str
    # price: float
    # lesson_duration_hours: int
    # lesson_in_week: int
    # lesson_place: str
    # lesson_type: str
    # lesson_language: str
    # lesson_audience: str
    # is_active: bool
    # is_confirmed: bool
    # is_promoted: bool
    # published: datetime
    # created_at: datetime
    # updated_at: datetime


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all():
    return Announcement(id="1", title="title")