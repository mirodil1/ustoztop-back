from src.db import db
from src.models import Tutor


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
    def update_tutor(cls, user_id, **tutor_new_data):
        tutor = cls.get_tutor_by_user_id(user_id=user_id)
        if tutor:
            for key, value in tutor_new_data.items():
                if hasattr(tutor, key):
                    setattr(tutor, key, value)
            db.session.add(tutor)
            db.session.commit()
        return None

    @classmethod
    def create_or_update_tutor_language(cls, user_id, *language_data):
        tutor = cls.get_tutor_by_user_id(user_id=user_id)
        for language in language_data:
            pass