from src.models import Tutor
from src.db import db

class TutorService:

    @staticmethod
    def create_tutor(user_id):
        tutor = Tutor(user_id=user_id)
        db.session.add(tutor)
        db.session.commit()

    @staticmethod
    def get_tutor_by_user_id(user_id):
        tutor = Tutor.query.filter_by(user_id=user_id).first()
