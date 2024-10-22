import os
from pathlib import Path

from flask import current_app as app
from werkzeug.utils import secure_filename

from src.db import db
from src.models import Education, Experience, Language, Tutor
from src.utils import allowed_file


class TutorService:

    @staticmethod
    def create_tutor(user_id):
        tutor = Tutor(user_id=user_id)
        db.session.add(tutor)
        db.session.commit()

    @staticmethod
    def get_tutor_by_user_id(user_id):
        tutor = Tutor.query.filter_by(user_id=user_id).first()
        if not tutor:
            return None
        return tutor

    @classmethod
    def update_tutor(
        cls, user_id: int, tutor_new_data: dict, files: dict | None = None,
    ):
        tutor = cls.get_tutor_by_user_id(user_id=user_id)
        if not tutor:
            return
        for key, value in tutor_new_data.items():
            if hasattr(tutor, key):
                setattr(tutor, key, value)
        if files:
            for file in files.values():
                if file  and allowed_file(file.filename):
                    file_name = secure_filename(file.filename)
                    folder_path = Path(app.config["UPLOAD_FOLDER"]) / "avatar"
                    folder_path.mkdir(parents=True, exist_ok=True)
                    file_path = folder_path / file_name

                    file.save(file_path )

                    tutor.avatar = str(file_path)
        db.session.add(tutor)
        db.session.commit()

    @classmethod
    def create_or_update_tutor_language(cls, user_id, *language_data):
        return cls.create_or_update_tutor_items(user_id, "experience", *language_data)

    @classmethod
    def create_or_update_tutor_experience(cls, user_id, *experience_data):
        return cls.create_or_update_tutor_items(user_id, "experience", *experience_data)

    @classmethod
    def create_or_update_tutor_education(cls, user_id, *education_data):
        return cls.create_or_update_tutor_items(user_id, "education", *education_data)

    @classmethod
    def create_or_update_tutor_items(cls, user_id, item_type, *item_data):
        tutor = cls.get_tutor_by_user_id(user_id=user_id)
        item_mapping = {item.id: item for item in getattr(tutor, item_type)}

        for item in item_data:
            if "id" in item:
                # Update existing item
                existing_item = item_mapping.get(item["id"])
                if existing_item:
                    for key, value in item.items():
                        if hasattr(existing_item, key):
                            setattr(existing_item, key, value)
            else:
                # Add new item
                new_item = None
                if item_type == "language":
                    new_item = Language(tutor_id=tutor.id, **item)
                elif item_type == "experience":
                    new_item = Experience(tutor_id=tutor.id, **item)
                elif item_type == "education":
                    new_item = Education(tutor_id=tutor.id, **item)

                if new_item:
                    db.session.add(new_item)

        # Delete items
        for item_id, item in item_mapping.items():
            if item_id not in [item.get("id") for item in item_data]:
                db.session.delete(item)

        db.session.commit()
