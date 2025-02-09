import base64
import uuid
import datetime

import httpx
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Depends
from slugify import slugify

from core.config import settings
from models.announcement import Announcement, Location
from schemas.announcement import (
    AnnouncementSchema,
    AnnouncementShortOutputSchema,
    AnnouncementStatusEnum,
)
from src.paginator import paginate_per_page
from db.postgres import get_db
from services.announcement_filter import AnnouncementFilter


class AnnouncementService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_announcements(
            self,
            filters: AnnouncementFilter,
            page: int,
            per_page: int,
            coords: list,
    ) -> list[AnnouncementSchema]:
        announcements = await self._get_active_announcements()

        user_gender = filters.gender
        role_name = filters.role
        ordering = filters.ordering

        filters.gender = None
        filters.role = None
        filters.ordering = None

        query = filters.filter(announcements)

        if user_gender or role_name:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.user_url}/api/v1/users/get/idx?gender={user_gender if user_gender else ''}&role={role_name if user_gender else ''}",
                )
                users = response.json()
                user_ids = []
                if response.status_code == 200:
                    user_ids = [user["id"] for user in users]
                query = query.filter(Announcement.user_id.in_(user_ids))

        if ordering.value == "-created_at":
            query=query.order_by(
                Announcement.created_at.desc(),
            )
        elif ordering.value == "price":
            query=query.order_by(
                Announcement.price.asc(),
            )
        elif ordering.value == "created_at":
            query=query.order_by(
                Announcement.created_at.asc(),
            )
        elif ordering.value == "-price":
            query=query.order_by(
                Announcement.price.desc(),
            )

        if coords and len(coords) == 2:
            lat, lng = coords[0], coords[1]
            radius = 10
            earth_radius_km = 6371

            haversine_distance = (
                earth_radius_km
                * func.acos(
                    func.cos(func.radians(lat)) * func.cos(
                        func.radians(Location.latitude),
                    )
                    * func.cos(func.radians(Location.longitude) - func.radians(lng))
                    + func.sin(func.radians(lat)) * func.sin(
                        func.radians(Location.latitude),
                    ),
                )
            )
            query = query.filter(haversine_distance <= radius)
            query = query.order_by(haversine_distance)

        paginated_announce = await paginate_per_page(query, page, per_page)

        announcement_list = [
            AnnouncementShortOutputSchema(
                id=announcement.id,
                name=announcement.name,
                slug=announcement.slug,
                user_id=announcement.user_id,
                user_info=await self._get_user_info(announcement.user_id),
                price=announcement.price,
                number_of_views=await self._get_views_count(announcement.id),
                location=announcement.location if announcement.location else None,
                is_promoted=announcement.is_promoted,
                description=announcement.description,
                created_at=announcement.created_at.date(),
            ) for announcement in paginated_announce["items"]
        ]

        return {
            "announcements": announcement_list,
            "count": paginated_announce["count"],
            "next_page": paginated_announce["next_page"],
            "previous_page": paginated_announce["previous_page"],
        }

    async def get_announcement_by_slug(
            self, slug: str, user_agent: str, user_id: int | None = None
    ) -> AnnouncementSchema:
        active = await self._get_active_announcements()
        announcement = active.filter(Announcement.slug==slug).scalar()
        if announcement:
            await self._add_views(announcement.id, user_agent)
        if not announcement:
            announcement = self.db.query(Announcement).filter(Announcement.slug == slug).scalar()
            if announcement and announcement.user_id == user_id:
                return announcement
        return announcement

    async def get_announcement_by_category(
        self,
        category_id: int,
    ) -> list[AnnouncementSchema]:
        active = await self._get_active_announcements()
        announcements = active.filter(Announcement.category_id==category_id).all()
        return announcements

    async def create_announcement(self, user_id: int, data: dict):
        # TODO: check for category existence by its id

        slug = f"{slugify(data.get('name'))}-{uuid.uuid4().hex[:6]}"
        location_data = data.pop("location")

        location = Location(**location_data)
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)

        announcement = Announcement(user_id=user_id, slug=slug)
        announcement.location_id = location.id
        for key, value in data.items():
            if hasattr(announcement, key):
                setattr(announcement, key, value)
        self.db.add(announcement)
        self.db.commit()

        return announcement
    
    async def update_announcement(self, user_id: int, announcement_id: int, data: dict):
        announcement = self.db.query(Announcement).filter(
            Announcement.id==announcement_id,
            Announcement.user_id==user_id
        ).scalar()
        if announcement:
            for key, value in data.items():
                if hasattr(announcement, key):
                    setattr(announcement, key, value)
            self.db.add(announcement)
            self.db.commit()
        return announcement

    async def get_user_announcement(
            self, user_id: int, status: str | None = AnnouncementStatusEnum.active,
    ):
        announcements = (
            self.db.query(Announcement)
                .filter(
                    Announcement.user_id==user_id,
                    Announcement.status==status,
                ).order_by(
                    Announcement.is_promoted.desc(),
                    Announcement.created_at.desc(),
                )
        )
        return announcements

    async def get_announcement_phone_number(self, announcement_id: int, user_agent: str):
        active = await self._get_active_announcements()
        announcement = active.filter(Announcement.id==announcement_id).scalar()
        if announcement:
            await self._add_phone_number_views(announcement_id, user_agent)
            return announcement.phone_number
        return None

    async def _get_active_announcements(self):
        announcements = (
            self.db.query(Announcement)
                .filter(
                    Announcement.status==AnnouncementStatusEnum.active,
                ).order_by(
                    Announcement.is_promoted.desc(),
                )
        )
        return announcements

    async def _add_views(self, announcement_id: int, user_agent: str):
        """
        Requesting to statistics service to add new views
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.stat_url}/api/v1/statistics/announcement_views/create/{announcement_id}",
                headers={"user-agent": user_agent},
            )
        return response

    async def _get_views_count(self, announcement_id: int):
        """
        Requesting to statistics service to retrieve views count
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.stat_url}/api/v1/statistics/announcement_veiws_count/{announcement_id}",
            )
            if response.status_code == 200:
                data = response.json()
                return data["count"]
            return None
    
    async def _get_phone_number_views_count(self, announcement_id: int):
        """
        Requesting to statistics service to retrieve views count
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.stat_url}/api/v1/statistics/phone_number_views/get/{announcement_id}",
            )
            if response.status_code == 200:
                data = response.json()
                return data["count"]
            return None

    async def _add_phone_number_views(self, announcement_id: int, user_agent: str):
        """
        Requesting to statistics service to add phone number views
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.stat_url}/api/v1/statistics/phone_number_views/create/{announcement_id}",
                headers={"user-agent": user_agent},
            )
            return response

    async def _get_user_info(self, user_id: int):
        """
        Requesting to users service to get user info
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.user_url}/api/v1/users/get/info/{user_id}"
            )
            if response.status_code == 200:
                return response.json()
            return None

    async def promote_announcement(self, data: str):
        announcement_id = data.get("ann_id")
        user_id = data.get("user_id")
        duration = data.get("duration")

        announcement = self.db.query(Announcement).filter(
            Announcement.id==announcement_id,
            Announcement.user_id==user_id,
        ).scalar()
        if announcement:
            start = datetime.datetime.now()
            expire = start + datetime.timedelta(days=duration)
            if not announcement.is_promoted:
                announcement.is_promoted = True
                announcement.promotion_started = start
                announcement.promotion_expired = expire
            else:
                announcement.promotion_expired = expire
            self.db.commit()
        return announcement

def get_announcement_service(db: Session = Depends(get_db)) -> AnnouncementService:
    return AnnouncementService(db)
