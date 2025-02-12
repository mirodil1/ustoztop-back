import datetime
import os
from pathlib import Path

from flask import current_app as app
from werkzeug.utils import secure_filename

from src.db import db
from src.models import Branch, LearningCenter, WorkingSchedule, Location
from src.utils import allowed_file
from src.exceptions import UnknownUser


class LearningCenterService:

    @staticmethod
    def create_center(user_id):
        learning_center = LearningCenter(user_id=user_id)
        db.session.add(learning_center)
        db.session.commit()

    @staticmethod
    def get_center_by_user_id(user_id):
        learning_center = LearningCenter.query.filter_by(user_id=user_id).first()
        if not learning_center:
            raise UnknownUser
        return learning_center

    @classmethod
    def update_center(
        cls, user_id, learning_center_new_data: dict, files: dict | None = None,
    ):
        learning_center = cls.get_center_by_user_id(user_id=user_id)
        if not learning_center:
            return
        for key, value in learning_center_new_data.items():
            if hasattr(learning_center, key):
                setattr(learning_center, key, value)
        if files:
            for field_name, file in files.items():
                # TODO: create new file manager service

                if file  and allowed_file(file.filename):
                    file_name = secure_filename(file.filename)
                    timestamp = datetime.datetime.now(datetime.UTC).strftime(
                        "%Y%m%d_%H%M%S"
                    )
                    file_name = f"{timestamp}_{file_name}"

                    if field_name == "avatar":
                        old_file = learning_center.avatar
                        folder_path = Path(app.config["UPLOAD_FOLDER"]) / "avatar"
                        learning_center.avatar = str(file_name)
                    elif field_name == "banner":
                        old_file = learning_center.banner or ""
                        folder_path = Path(app.config["UPLOAD_FOLDER"]) / "banner"
                        learning_center.banner = str(file_name)

                    folder_path.mkdir(parents=True, exist_ok=True)

                    file_path = folder_path / file_name
                    file.save(file_path)
                    if old_file:
                        Path(folder_path / old_file).unlink(missing_ok=True)

        db.session.add(learning_center)
        db.session.commit()

    @classmethod
    def create_or_update_center_branch(cls, user_id, *branch_data):
        return cls.create_or_update_center_items(user_id, "branch", *branch_data)

    @classmethod
    def create_or_update_center_schedule(cls, user_id, *schedule_data):
        return cls.create_or_update_center_items(
            user_id, "working_schedule", *schedule_data)

    @classmethod
    def create_or_update_center_items(cls, user_id, item_type, *item_data):
        learning_center = cls.get_center_by_user_id(user_id=user_id)
        item_mapping = {item.id: item for item in getattr(learning_center, item_type)}

        for item in item_data:
            if "id" in item:
                # Update existing item
                existing_item = item_mapping.get(item["id"])
                if existing_item:
                    if item_type=="branch":
                        location_data = item.pop("location", None)
                        if location_data:
                            location = Location(**location_data)
                            db.session.add(location)
                            new_item.location = location
                    for key, value in item.items():
                        if hasattr(existing_item, key):
                            setattr(existing_item, key, value)
            else:
                # Add new item
                new_item = None
                if item_type == "branch":
                    location_data = item.pop("location", None)
                    if location_data:
                        location = Location(**location_data)
                        db.session.add(location)
                    new_item = Branch(learning_center_id=learning_center.id, **item)
                    new_item.location = location

                elif item_type == "working_schedule":
                    new_item = WorkingSchedule(
                        learning_center_id=learning_center.id,
                        **item,
                    )

                if new_item:
                    db.session.add(new_item)

        # Delete items
        for item_id, item in item_mapping.items():
            if item_id not in [item.get("id") for item in item_data]:
                db.session.delete(item)

        db.session.commit()
