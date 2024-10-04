from src.models import LearningCenter
from src.db import db

class LearningCenterService:

    @staticmethod
    def create_center(user_id):
        learning_center = LearningCenter(user_id=user_id)
        db.session.add(learning_center)
        db.session.commit()
