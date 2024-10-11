from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from src import schemas
from src.routes.v1 import router
from src.services.tutor import TutorService


@router.route("/get/tutor/<int:user_id>", methods=["GET"])
def get_tutor(user_id):
    tutor = TutorService.get_tutor_by_user_id(user_id=user_id)
    print(tutor)
    return tutor, 200

